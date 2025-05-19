# Import BaseModel from pydantic
from pydantic import BaseModel
from typing import List, Dict, Any


# Define TextSubmission model
# - Fields: text: str
class TextSubmission(BaseModel):
    """
    Model to represent a text submission for redaction.
    """

    text: str


# Define JobStatus model
# - Fields: job_id: str, status: str
class JobStatus(BaseModel):
    """
    Model to represent the status of a job.
    """

    job_id: int
    status: str


# Define RedactedResult model
# - Fields: job_id: str, redacted_text: str, metadata: list/dict
class RedactedResult(BaseModel):
    """
    Model to represent the result of a redaction job.
    """

    job_id: int
    redacted_text: str
    metadata: List[Dict[str, Any]]


class JobStore:
    """
    In-memory job store to track job status and results.
    """

    def __init__(self):
        self.store: Dict[int, Dict[str, Any]] = {}

    def add_job(self, job_id: int, status: str, result: RedactedResult):
        self.store[job_id] = {"status": status, "result": result}

    def get_job(self, job_id: int) -> Dict[str, Any]:
        if job_id in self.store:
            return self.store[job_id]
        else:
            raise ValueError(f"Job ID {job_id} not found in store.")

    def update_job_status(self, job_id: int, status: str):
        if job_id in self.store:
            self.store[job_id]["status"] = status
        else:
            raise ValueError(f"Job ID {job_id} not found in store.")
