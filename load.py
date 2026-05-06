# pylint: skip-file

#imports
import os
from dotenv import load_dotenv
import boto3
import logging
from datetime import datetime
from pathlib import Path
from modules.extract_json_files import upload_json_to_S3

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

# #read in JSON from output
# json_files = os.listdir('output')

#save data into S3 bucket
local_path = './output/test_upload.json'
s3_filename = 'python-import/test_upload.json'

upload_json_to_S3(local_path=local_path, bucket=bucket, s3_filename=s3_filename)