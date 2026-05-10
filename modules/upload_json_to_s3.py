# pylint: skip-file

#imports
import os
import logging
import boto3

log = logging.getLogger(__name__)
from pathlib import Path

#Function
def load(AWS_KEY_ID, AWS_SECRET_KEY, BUCKET, BUCKET_OBJECT, data_dir):
    """This will load any json files in the data directory to a specified S3 bucket.


    Args:
        aws_key (string): AWS access key attached to an IAM User, with relevant permissions.
        aws_secret (string): AWS secret access key attached to an IAM User, with relevant permissions. 
        bucket (string): S3 bucket to load the data into.
        data_dir (string): The data directory where the data is located. This must be a full filepath e.g. Path('data')
    """

    if not AWS_KEY_ID or not AWS_SECRET_KEY:
        log.error("AWS credentials missing. Check AWS_API_KEY and AWS_SECRET_KEY in environment variables.")
    else:
        log.info("AWS credentials loaded successfully.")

    #configure S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id = AWS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_KEY
    )

    #read in JSON from the output data directory
    files = list(data_dir.glob(f'*.json'))

    #loop through the data directory and upload to S3
    processed = 0
    for file in files:
        filename = os.path.basename(file)
        s3_filename = f'{BUCKET_OBJECT}/{filename}'

        try:
            s3_client.upload_file(file,BUCKET,s3_filename)
            print(f"{s3_filename} uploaded to the S3 bucket: {BUCKET}")
            log.info(f'{file} uploaded to S3')
            s3_client.head_object(Bucket=BUCKET,Key=s3_filename)
            os.remove(file)
            log.info(f'{file} deleted locally from {data_dir}')
            processed +=1
        except Exception as e:
                log.error(e)

    log.info(f'{processed} files uploaded to {BUCKET}/{BUCKET_OBJECT}')