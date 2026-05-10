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
start_time = '20260428T00'
end_time = '20260429T23'
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


#
if extractJsonFiles(url,params,API_KEY,API_SECRET_KEY,'output'):
    data_dir = Path('output')
    loadJson(AWS_KEY_ID, AWS_SECRET_KEY, BUCKET, BUCKET_OBJECT, data_dir)
    log.info('Scripts ran successfully')
    print('Scripts ran successfully')
else:
    log.error('Extract failed. Script stopped.')
    print('Extract failed. Script stopped.')