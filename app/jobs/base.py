from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import uuid
from enum import Enum

class JobStatus(Enum):
    UNSTARTED = "unstarted"
    STARTED = "started" # Job has been sent to backend
    RUNNING = "running" # Job is running on backend
    COMPLETED = "completed" # Job has completed
    FAILED = "failed" # Job has failed

class BaseJobUpdate(BaseModel):
    job_id: uuid.UUID
    status: JobStatus
    output: Optional[Dict[str, Any]]

    def to_json_dict(self):
        output = {}

        # Add attributes to output based on job_params
        for key, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, uuid.UUID):
                    output[key] = str(value)
                elif isinstance(value, Enum):
                    output[key] = value.value
                else:
                    output[key] = value

        return output

class BaseJob(BaseModel):
    status: JobStatus = JobStatus.STARTED
    model_name: str = "cjim8889/AllysMix3"
    output: Optional[Dict[str, Any]] = None
    job_id: uuid.UUID = Field(default_factory=uuid.uuid4)