# Import BaseModel from pydantic
from pydantic import BaseModel
from typing import List, Dict, Any


# Define TextSubmission model
# - Fields: text: str
class TextSubmission(BaseModel):
    text: str


# Define JobStatus model
# - Fields: job_id: str, status: str
class JobStatus(BaseModel):
    job_id: int
    status: str


# Define RedactedResult model
# - Fields: job_id: str, redacted_text: str, metadata: list/dict
class RedactedResult(BaseModel):
    job_id: int
    redacted_text: str
    metadata: List[Dict[str, Any]]
