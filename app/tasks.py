# Import asyncio and maintain an in-memory dict of job_id → status/results
import asyncio
from typing import Dict, Any
from pydantic import BaseModel
from redact import sanitize_text
from models import TextSubmission, JobStatus, RedactedResult
from logger import logger

# In-memory job store: job_id -> status/results
job_store: Dict[int, Dict[str, Any]] = {}


# Define a coroutine to perform redaction
# - Accept job_id and input text
# - Call redact.py logic
# - Store result and mark job complete
async def redact_text(job_id: str, text: str) -> Dict[str, Any]:
    # Simulate redaction process
    JobStatus(job_id=job_id, status=f"processing job {job_id}")
    await asyncio.sleep(2)  # Simulate processing time

    redacted_text, metadata = sanitize_text(text)
    # Store result in job store
    result = {
        "status": "completed",
        "result": RedactedResult(
            job_id=job_id, redacted_text=redacted_text, metadata=metadata
        ),
    }
    job_store[int(job_id)] = result
    JobStatus(job_id=job_id, status="completed")
    return result


# Define an async-safe job queue mechanism
job_queue = asyncio.Queue()


async def job_worker():
    """
    Worker coroutine to process jobs from the queue.
    """
    while True:
        job_id, text = await job_queue.get()
        try:
            logger.info(f"Processing job {job_id}")
            await redact_text(job_id, text)
        except Exception as e:
            logger.error(f"Error processing job {job_id}: {e}")
            job_store[int(job_id)] = {"status": "failed", "error": str(e)}
        finally:
            job_queue.task_done()


def submit_job(text: str) -> int:
    """
    Submit a new redaction job and return the job_id.
    """
    job_id = len(job_store) + 1
    job_store[job_id] = {"status": "queued"}
    asyncio.create_task(job_queue.put((job_id, text)))
    logger.info(f"Job {job_id} submitted")
    return job_id


def get_job_status(job_id: str) -> Dict[str, Any]:
    """
    Retrieve the status or result of a job.
    """
    return job_store.get(int(job_id), {"status": "not_found"})
