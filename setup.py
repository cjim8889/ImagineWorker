from app.jobs.txt2img import TextToImageJob
from app.components.model import Model
from app.env import *

model = Model(
    model_name_or_path=MODEL_NAME
)

model.inference(
    job=TextToImageJob(
        job_id="startup",
        prompt="Startup idea:",
        face_restore=True,
        num_inference_steps=1,
    )   
)