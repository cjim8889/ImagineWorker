from .s3 import Storage
from app.env import *

s3 = Storage(
    key_id=aws_access_key_id,
    key=aws_secret_access_key,
    endpoint=s3_endpoint_url,
    bucket_name=bucket_name,
)