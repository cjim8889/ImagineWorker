import os

aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
s3_endpoint_url=os.environ.get('S3_ENDPOINT_URL')
bucket_name=os.environ.get('S3_BUCKET_NAME')
JOB_TYPE=os.environ.get('JOB_TYPE', 'TextToImageJob')
MODEL_NAME=os.environ.get('MODEL_NAME', 'cjim8889/AllysMix3')
BEARER_TOKEN=os.environ.get('BEARER_TOKEN')
BACKEND_ENDPOINT=os.environ.get('BACKEND_ENDPOINT')