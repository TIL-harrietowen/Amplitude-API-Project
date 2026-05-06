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
import time

#----------------------------------------------------------------------------------------------------------#
# Create and set log filepath location
log_dir = './logs'
os.makedirs(log_dir, exist_ok=True)
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_filename = f"{log_dir}/Amplitude_Extract_{timestamp}.log"

#Set logging configuration
logging.basicConfig(
    filename=log_filename,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

log = logging.getLogger()
log.info('Logger intialised')

#----------------------------------------------------------------------------------------------------------#
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

#----------------------------------------------------------------------------------------------------------#
#variables required for API response handling
status = response.status_code
temp_dir = "./temp"
data_dir = "./output"
processed = 0

if 200 <= status < 300:
    print(f"Connection was successful, status code: {status}")
    log.info(f"API connection was successful, status code: {status}.")

    #read file into memory
    file_object = io.BytesIO(response.content)
    log.info("Response content loaded into memory")

    #first zip file extraction into a temporary directory  
    with zipfile.ZipFile(file_object) as z:
        z.extractall(temp_dir)
        log.info(f".gz files extracted into the temp directory: {temp_dir}")

        #second zip file extraction into an data output directory
        log.info(f"Starting to read and extract files inside {temp_dir}")
        for name in z.namelist():

            #read in the .gz files as bytes from the temporary directory
            with gzip.open(f"{temp_dir}/{name}", 'rb') as f:

                #create variables for the name and location to output .gz files to
                output_name = os.path.basename(name)[:-3]
                output_path = f"{data_dir}/{output_name}"

                #create the data output directory
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                #write the json files to the new output folder
                with open(output_path, "wb") as files:
                    shutil.copyfileobj(f, files)
                
                #count the number of files processed
                processed +=1
        
        log.info(f"Finished processing {processed} file(s)")

        #delete the temp folder to clean up
        shutil.rmtree(temp_dir)
        log.info(f"Temporary folder deleted: {temp_dir}")

else:
    print(f"Error: {status} {response.get("message", "no message found")}")
    log.error(f"Error: {status} {response.get("message", "no message found")}")

log.info("API Extraction Finished")