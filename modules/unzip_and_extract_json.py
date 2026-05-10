# pylint: skip-file

#imports
import os
import requests

import io
import zipfile
import gzip
import shutil

import logging
from datetime import datetime

log = logging.getLogger(__name__)

def extract_json_files(url,params,API_KEY,API_SECRET_KEY,data_dir):
    """This function will unzip a file into a temporary folder and then unzip all .gz files into a desired directory.
        The temporary folder will be deleted afterwards.

    Args:
        url (string): URL of the API to call.
        params (dictionary): a dictionary of the parameters to include in the API call e.g. start and end time.
        API_KEY (string): the access key required to authenticate the API.
        API_SECRET_KEY (string): the secret access key required to authenticate the API.
        data_dir (string): the directory of where the data should be stored after unzipping.
    """
    #variables required for API response handling
    response = requests.get(url, params=params, auth=(API_KEY, API_SECRET_KEY))
    status = response.status_code
    temp_dir = "./temp"

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

            return True

    else:
        print(f"Error: {status} {response.get("message", "no message found")}")
        log.error(f"Error: {status} {response.get("message", "no message found")}")

    log.info("API Extraction Finished")