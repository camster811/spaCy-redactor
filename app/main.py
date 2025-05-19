# Import FastAPI and background task system
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import uuid


# Initialize FastAPI instance
app = FastAPI()

# Import Pydantic models from models.py
from models import TextSubmission, JobStatus, RedactedResult, JobStore
from tasks import redact_text


# Simulate in-memory job tracking store (dict or similar)
job_store = JobStore()  # job_id: {"status": str, "result": RedactedResult}


async def run_redaction_task(job_id: str, text: str):
    try:
        redacted_result = await redact_text(job_id, text)
        result = redacted_result["result"]

        job_store.add_job(job_id, "completed", result=result)
    except Exception as e:
        job_store.add_job(
            job_id,
            "failed",
            RedactedResult(
                job_id=job_id,
                redacted_text="",
                metadata=[{"error": str(e)}],
            ),
        )


# Define POST /submit
# - Accepts a text blob
# - Kicks off async redaction task
# - Returns job_id
@app.post("/submit")
async def submit_text(
    text_submission: TextSubmission, background_tasks: BackgroundTasks
):
    job_id = str(uuid.uuid4())
    job_store.add_job(
        job_id,
        "queued",
        RedactedResult(job_id=job_id, redacted_text="", metadata=[]),
    )  # Initialize job status
    background_tasks.add_task(run_redaction_task, job_id, text_submission.text)
    return JSONResponse(
        content={"job_id": job_id},
        status_code=202,
    )


# Define GET /status/{job_id}
# - Returns current job status
@app.get("/status/{job_id}")
async def get_job_status(job_id: str):
    try:
        job = job_store.get_job(job_id)
        return JSONResponse(
            content={
                "job_id": job_id,
                "status": job["status"],
            },
            status_code=200,
        )
    except ValueError:
        return JSONResponse(
            content={"error": "Job ID not found"},
            status_code=404,
        )


# Define GET /result/{job_id}
# - Returns redacted output if complete
@app.get("/result/{job_id}")
async def get_redacted_result(job_id: str):
    try:
        job = job_store.get_job(job_id)
        if job["status"] == "completed":
            return JSONResponse(
                content={
                    "job_id": job_id,
                    "redacted_text": job["result"].redacted_text,
                    "metadata": job["result"].metadata,
                },
                status_code=200,
            )
        elif job["status"] == "queued":
            return JSONResponse(
                content={"error": "Job not completed yet"},
                status_code=202,
            )
        elif job["status"] == "failed":
            return JSONResponse(
                content={
                    "error": "Job failed",
                    "details": job["result"].metadata,
                },
                status_code=500,
            )
        else:
            return JSONResponse(
                content={"error": "unknown job status"},
                status_code=202,
            )
    except ValueError:
        return JSONResponse(
            content={"error": "Job ID not found"},
            status_code=404,
        )


# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
