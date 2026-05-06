# pylint: skip-file

#imports
import os
from dotenv import load_dotenv
import boto3
import logging
from datetime import datetime
from pathlib import Path


#----------------------------------------------------------------------------------------------------------#
# Create and set log filepath location
log_dir = './logs'
os.makedirs(log_dir, exist_ok=True)
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_filename = f"{log_dir}/Amplitude_Load_{timestamp}.log"

#Set logging configuration
logging.basicConfig(
    filename=log_filename,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

log = logging.getLogger()
log.info('Logger intialised')

#----------------------------------------------------------------------------------------------------------#
#load in environment variables
load_dotenv()
log.info("Environment variables loaded")

#----------------------------------------------------------------------------------------------------------#
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

#read in JSON from the output data directory
data_dir = Path('output')
files = list(data_dir.glob(f'*.json'))

#loop through the data directory and upload to S3
processed = 0
for file in files:
    filename = os.path.basename(file)
    s3_filename = f'{bucket_object}/{filename}'

    try:
        s3_client.upload_file(file,bucket,s3_filename)
        print(f"{s3_filename} uploaded to the S3 bucket: {bucket}")
        log.info(f'{file} uploaded to S3')
        s3_client.head_object(Bucket=bucket,Key=s3_filename)
        os.remove(file)
        log.info(f'{file} deleted locally from {data_dir}')
        processed +=1
    except Exception as e:
            log.error(e)

log.info(f'Finished uploading {processed} files')
