# pylint: skip-file

#imports
from modules.setup_logging import setupLogging
from modules.unzip_and_extract_json import extractJsonFiles
from modules.upload_json_to_s3 import loadJson

from dotenv import load_dotenv
import requests
import os
from pathlib import Path

#logging
log = setupLogging('logs')

#load environment variables
load_dotenv()
log.info("Environment Variables Read")

#Load API Info
API_KEY = os.getenv('AMP_API_KEY')
API_SECRET_KEY = os.getenv('AMP_SECRET_KEY')
start_time = '20260514T02'
end_time = '20260514T03'
log.info(f"Export window set: start={start_time}, end={end_time}")

#API request setup
url = 'https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': start_time,
    'end': end_time
}

#Load AWS Info
AWS_KEY_ID = os.getenv('AWS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
BUCKET = os.getenv('BUCKET')
BUCKET_OBJECT = os.getenv('BUCKET_OBJECT')

#GET request
log.info(f"Sending GET request to {url}")
response = requests.get(url, params=params, auth=(API_KEY, API_SECRET_KEY))
log.info(f"Response received, content size: {len(response.content)} bytes")


#extract JSON files from the Amplitude API response and upload them to S3
if extractJsonFiles(url,params,API_KEY,API_SECRET_KEY,'output'):
#if the extract step succeeds, the JSON files in the output directory are uploaded to the configured S3 bucket
    data_dir = Path('output')
    loadJson(AWS_KEY_ID, AWS_SECRET_KEY, BUCKET, BUCKET_OBJECT, data_dir)
    log.info('Scripts ran successfully')
    print('Scripts ran successfully')
#if the extract step fails, the script stops and logs the error
else:
    log.error('Extract failed. Script stopped.')
    print('Extract failed. Script stopped.')