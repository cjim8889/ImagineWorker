from app.env import *
from .dispatcher import Dispatcher
from .base  import BaseJob, JobStatus


dispatcher = Dispatcher(
    backend_endpoint=BACKEND_ENDPOINT,
    job_type=JOB_TYPE,
    model_name=MODEL_NAME,
)