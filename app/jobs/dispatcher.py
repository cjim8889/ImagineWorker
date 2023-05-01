import requests
from requests.exceptions import HTTPError
from app.env import BEARER_TOKEN
from .txt2img import TextToImageJob
from .base import BaseJob, BaseJobUpdate
from app.logger import logger
import time

class Dispatcher:
    def __init__(
        self,
        backend_endpoint: str,
        job_type: str,
        model_name: str,
    ) -> None:
        self.backend_endpoint = backend_endpoint
        self.job_type = job_type
        self.model_name = model_name
        self.headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}

    def generate_get_job_url(self):
        return f"{self.backend_endpoint}/api/v1/passive/"

    def generate_update_job_url(self):
        return f"{self.backend_endpoint}/api/v1/passive/update"

    def generate_get_job_params(self):
        return {
            "job_type": self.job_type,
            "model_name": self.model_name,
        }
    
    def update_job(self, job: BaseJob):
        try:
            r = requests.put(
                self.generate_update_job_url(),
                json=BaseJobUpdate(**job.dict()).to_json_dict(),
                headers=self.headers,
            )
            r.raise_for_status()
        except Exception as e:
            logger.error(f"Error updating Job {job.job_id}: {e}")
            raise e

    def get_job_or_block(self) -> BaseJob:
        while True:
            try:
                r = requests.get(
                    self.generate_get_job_url(),
                    params=self.generate_get_job_params(),
                    headers=self.headers,
                )
                r.raise_for_status()
                return TextToImageJob(**r.json())
            except HTTPError as e:
                if e.response.status_code == 404:
                    logger.info("No job found, waiting...")
                    time.sleep(1)
                else:
                    logger.error(f"Error getting job from backend: {e}")
                    time.sleep(1)
            except Exception as e:
                logger.error(f"Error getting job from backend: {e}")
                time.sleep(1)
