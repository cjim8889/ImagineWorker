from app.env import *
from typing import Optional
from .base import BaseJob
from pydantic import create_model

# Define a list of acceptable parameters
txt2img_job_params = [
    ('prompt', str, ...),
    ('model_name', str, MODEL_NAME),
    ('negative_prompt', Optional[str], None),
    ('scheduler', Optional[str], "DPMSolverMultistepScheduler"),
    ('num_inference_steps', Optional[int], 30),
    ('guidance_scale', Optional[float], 8.0),
    ('seed', Optional[int], None),
    ('width', Optional[int], 512),
    ('height', Optional[int], 512),
    ('upsample', Optional[bool], False),
    ('face_restore', Optional[bool], False),
    ('codeformer_fidelity', Optional[float], 0.6),
]

TextToImageParams = create_model(
    "TextToImageParams",
    **{name: (type_, default) for name, type_, default in txt2img_job_params},
)

TextToImageJob = create_model(
    "TextToImageJob",
    **{name: (type_, default) for name, type_, default in txt2img_job_params},
    __base__=BaseJob,
)