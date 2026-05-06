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

def extract_json_files():
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