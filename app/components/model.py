from .codeformer import setup_codeformer, codeformer_inference
from app.jobs import BaseJob
from app.logger import logger
from diffusers import DiffusionPipeline
from typing import Tuple
from PIL import Image
import numpy as np
import cv2
import time
import torch


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class Model:
    def __init__(self, model_name_or_path: str) -> None:
        self.upsampler, self.codeformer_net = setup_codeformer()
        self.model = DiffusionPipeline.from_pretrained(
            model_name_or_path,
            custom_pipeline="lpw_stable_diffusion",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        ).to(device)

        self.allowed_model_params = set([
            "prompt",
            "negative_prompt",
            "num_inference_steps",
            "guidance_scale",
            "seed",
            "width",
            "height",
        ])
        self.available_schedulers = {v.__name__: v for v in self.model.scheduler.compatibles}
        self.current_scheduler = self.model.scheduler.__class__.__name__

    def switch_scheduler(self, scheduler_name):
        if scheduler_name == self.current_scheduler or scheduler_name is None:
            return
        
        if scheduler_name not in self.available_schedulers:
            logger.info(f"Error: {scheduler_name} is not a valid scheduler. Using {self.current_scheduler} instead")
            return

        is_karras = False
        if "Karras" in scheduler_name:
            scheduler_name = scheduler_name.replace("Karras", "")
            is_karras = True

        self.model.scheduler = self.available_schedulers[scheduler_name].from_config(self.model.scheduler.config)
        if is_karras and hasattr(self.model.scheduler, "use_karras_sigmas"):
            self.model.scheduler.use_karras_sigmas = True

        self.current_scheduler = scheduler_name
        logger.info(f"Switched to {self.current_scheduler}")

    def filter_allowed_model_params(self, params: dict) -> dict:
        if "seed" in params:
            params["seed"] = torch.cuda.manual_seed(params["seed"])
            
        return {k: v for k, v in params.items() if k in self.allowed_model_params}

    def inference(self, job: BaseJob) -> Tuple[Image.Image, float]:
        logger.info(f"Starting inference for Job: {job.job_id}")
        start_time = time.time()

        try:
            image = self._inference(job)
        except Exception as e:
            logger.error(f"Error during inference for Job: {job.job_id}")
            raise e
        
        elapsed_time = (time.time() - start_time) * 1000
        logger.info(f"Finished inference for Job: {job.job_id} in {elapsed_time:.2f}ms")

        return image, elapsed_time

    def _inference(self, job: BaseJob) -> Image.Image:
        if hasattr(job, "scheduler"):
            self.switch_scheduler(job.scheduler)

        filtered_kwargs = {k: v for k, v in job.dict().items() if v is not None}
        logger.info(f"Running inference with kwargs: {filtered_kwargs} for Job: {job.job_id}")
        
        image = self.model(
            **self.filter_allowed_model_params(filtered_kwargs),
        ).images[0]

        if hasattr(job, "face_restore") and job.face_restore:
            image, _ = codeformer_inference(
                upsampler=self.upsampler,
                codeformer_net=self.codeformer_net,
                image=image,
                background_enhance=True,
                face_upsample=True,
                upscale=4,
                codeformer_fidelity=job.codeformer_fidelity if hasattr(job, "codeformer_fidelity") else 0.6,
            )

        elif hasattr(job, "upsample") and job.upsample:
            img = np.array(image)
            # Convert the image from RGB to BGR format (OpenCV uses BGR by default)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            img = self.upsampler.enhance(img, outscale=4)[0]
            restored_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Convert the numpy.ndarray image to a PIL.Image.Image object
            image = Image.fromarray(restored_img)

        return image