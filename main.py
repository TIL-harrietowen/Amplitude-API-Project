# pylint: skip-file

#imports
import os
import requests
from dotenv import load_dotenv

import json
import io
import zipfile
import gzip
import shutil

import logging
from datetime import datetime

# Create and set log filepath location
log_dir = './logs'
os.makedirs(log_dir, exist_ok=True)
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_filename = f"{log_dir}/Amplitude_Extract_{timestamp}.log"

# Configure logs to retrieve INFO messages and higher
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
)

log = logging.getLogger()
log.info(f"Logging initialised, writing to {log_filename}")

#load environment variables
load_dotenv()
log.info("Environment Variables Read")

#load api credentials
api_key = os.getenv('AMP_API_KEY')
api_secret = os.getenv('AMP_SECRET_KEY')

if not api_key or not api_secret:
    log.error("API credentials missing. Check AMP_API_KEY and AMP_SECRET_KEY in environment variables.")
else:
    log.info("API credentials loaded successfully.")

#API parameters
start_time = '20260428T00'
end_time = '20260429T23'
log.info(f"Export window set: start={start_time}, end={end_time}")

#API request setup
url = 'https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': start_time,
    'end': end_time
}

#GET request
log.info(f"Sending GET request to {url}")
response = requests.get(url, params=params, auth=(api_key, api_secret))
log.info(f"Response received, content size: {len(response.content)} bytes")

#check API response
status = response.status_code
if status != 200:
    print(f"Connection was unsuccessful, status_code: {status}")
    log.error(f"API connection was unsuccessful, status code: {status}.")

else:
    print(f"Connection was successful, status code: {status}")
    log.info(f"API connection was successful, status code: {status}.")

    #read file in memory
    file_object = io.BytesIO(response.content)
    log.info("Response content loaded in memory")
        
    with zipfile.ZipFile(file_object) as z:
        #extract the files into a temp folder
        temp_path = "./temp"
        z.extractall(temp_path)
        log.info(f".gz files extracted to temp folder: {temp_path}")

        #loop through each .gz file
        processed = 0
        for name in z.namelist():
            #read the .gz files
            with gzip.open(f"{temp_path}/{name}", 'rb') as f:
                log.info(".gz files read")
                #create the name and location to output .gz files
                output_name = os.path.basename(name)[:-3]
                output_path = f"./output/{output_name}"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                log.info(f"Output directory created: {os.path.dirname(output_path)}")
                #write the json files to the new output folder
                with open(output_path, "wb") as files:
                    shutil.copyfileobj(f, files)
                processed +=1
        
        log.info(f"Finished processing {processed} file(s)")

        #delete the temp folder to clean up
        shutil.rmtree(temp_path)
        log.info(f"Temporary folder deleted: {temp_path}")

log.info("API Extraction Finished")