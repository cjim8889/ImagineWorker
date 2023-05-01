import boto3
from app.env import *
from PIL import Image
from io import BytesIO
from app.logger import logger


class Storage:
    def __init__(
        self,
        key_id: str = aws_access_key_id,
        key: str = aws_secret_access_key,
        endpoint: str = s3_endpoint_url,
        bucket_name: str = bucket_name,
    ) -> None:
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=key_id,
            aws_secret_access_key=key,
            endpoint_url=endpoint,
        )
        self.endpoint = endpoint
        self.bucket_name = bucket_name

    def generate_public_url(self, filename):
        return f"{self.endpoint}/{self.bucket_name}/{filename}"
    
    def upload_image(self, filename: str, image: Image):
        try:
            # Save PIL image to in-memory file
            in_mem_file = BytesIO()
            image.save(in_mem_file, format="JPEG")
            in_mem_file.seek(0)

            # Upload the in-memory file to S3
            self.s3.upload_fileobj(
                in_mem_file,
                self.bucket_name,
                filename,
                ExtraArgs={"ContentType": "image/jpeg", "ACL": "public-read"},
            )

            # Generate a public URL for the image
            return self.generate_public_url(filename)
        
        except Exception as e:
            logger.error(f"Error uploading image to S3: {e}")
            raise e
