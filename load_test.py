# pylint: skip-file

#imports
import os
from dotenv import load_dotenv
import boto3
import logging
from datetime import datetime
from pathlib import Path

#load environment variables
load_dotenv()

#logging config

#AWS variables
aws_key = os.getenv('AWS_KEY_ID')
aws_secret = os.getenv('AWS_SECRET_KEY')
bucket = os.getenv('BUCKET')
bucket_object = os.getenv('BUCKET_OBJECT')

#configure S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id = aws_key,
    aws_secret_access_key = aws_secret
)

#save data into S3 bucket
local_path = 'output/100011471/100011471_2026-04-28_0#0.json'
s3_filename = 'python-import/100011471_2026-04-28_0#0.json'

s3_client.upload_file(local_path, bucket, s3_filename)