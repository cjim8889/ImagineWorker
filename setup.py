from app.jobs.txt2img import TextToImageJob
from app.components.model import Model
import uuid
from app.env import *

model = Model(
    model_name_or_path=MODEL_NAME
)
