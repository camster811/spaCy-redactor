# Import FastAPI and background task system
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import uuid


# Initialize FastAPI instance
app = FastAPI()

# Import Pydantic models from models.py
from models import TextSubmission, JobStatus, RedactedResult
from tasks import redact_text

# Simulate in-memory job tracking store (dict or similar)
job_store = {}  # job_id: {"status": str, "result": RedactedResult}


async def run_redaction_task(job_id: str, text: str):
    try:
        redacted_result = await redact_text(job_id, text)
        # If redact_text returns a dict, extract the string value for redacted_text
        redacted_text_str = (
            redacted_result["redacted_text"]
            if isinstance(redacted_result, dict)
            else redacted_result
        )
        job_store[job_id] = {
            "status": "completed",
            "result": RedactedResult(
                job_id=job_id,
                redacted_text=redacted_text_str,
                metadata=[],
            ),
        }
    except Exception as e:
        job_store[job_id]["status"] = "failed"
        job_store[job_id]["result"] = {"error": str(e)}


# Define POST /submit
# - Accepts a text blob
# - Kicks off async redaction task
# - Returns job_id
@app.post("/submit")
async def submit_text(
    text_submission: TextSubmission, background_tasks: BackgroundTasks
):
    job_id = str(uuid.uuid4())
    job_store[job_id] = {"status": "queued", "result": None}
    background_tasks.add_task(run_redaction_task, job_id, text_submission.text)
    return JSONResponse(
        content={"job_id": job_id},
        status_code=202,
    )


# Define GET /status/{job_id}
# - Returns current job status
@app.get("/status/{job_id}")
async def get_job_status(job_id: str):
    if job_id in job_store:
        status = job_store[job_id]["status"]
        return JSONResponse(
            content={"job_id": job_id, "status": status},
            status_code=200,
        )
    else:
        return JSONResponse(
            content={"error": "Job ID not found"},
            status_code=404,
        )


# Define GET /result/{job_id}
# - Returns redacted output if complete
@app.get("/result/{job_id}")
async def get_redacted_result(job_id: str):
    print(f"Fetching result for job_id: {job_id}")


# Include logic to start async task using create_task from asyncio
