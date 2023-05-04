from app.jobs import dispatcher, JobStatus, TextToImageJob
from app.logger import logger
from app.components.model import Model
from app.env import *
from app.components import s3
import runpod

model = Model(model_name_or_path=MODEL_NAME)


def run_runpod(event):
    if "input" not in event:
        raise ValueError("No input provided")

    job = TextToImageJob(**event["input"])
    logger.info(f"Got job: {job}")

    try:
        image, elapsed_time = model.inference(job)
        logger.info(f"Generated image in {elapsed_time} seconds")

        image_url = s3.upload_image(image=image, filename=f"{job.job_id}.jpg")
        logger.info(f"Uploaded image to {image_url}")
    except Exception as e:
        logger.error(f"Error processing Job {job.job_id}: {e}")
        raise e

    return {
        "image_url": image_url,
        "elapsed_time": elapsed_time,
    }


def run():
    while True:
        job = dispatcher.get_job_or_block()
        logger.info(f"Got job: {job}")

        try:
            image, elapsed_time = model.inference(job)
            logger.info(f"Generated image in {elapsed_time} seconds")

            image_url = s3.upload_image(image=image, filename=f"{job.job_id}.jpg")
            logger.info(f"Uploaded image to {image_url}")
        except Exception as e:
            logger.error(f"Error processing Job {job.job_id}: {e}")
            job.status = JobStatus.FAILED
            job.output = {
                "error": str(e),
            }
            dispatcher.update_job(job)
            continue

        job.status = JobStatus.COMPLETED
        job.output = {
            "image_url": image_url,
            "elapsed_time": elapsed_time,
        }

        dispatcher.update_job(job)


if __name__ == "__main__":
    logger.info("Starting job loop...")
    if IS_RUNPOD:
        runpod.serverless.start({"handler": run_runpod})
    else:
        run()
