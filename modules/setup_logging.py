# pylint: skip-file

#imports
import os
import logging
from datetime import datetime
import time

#----------------------------------------------------------------------------------------------------------#

def setupLogging(log_dir):
    """A function that will configure logging in a python script.
        Level of logging available: INFO and above.

    Args:
        log_dir (string): the file path that you want the log files to be saved to.
    """
    # Create log directory and set log file names
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = os.path.join(log_dir,f'{timestamp}.log')

    #Set logging configuration
    logging.basicConfig(
        filename=log_filename,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    return logging.getLogger('Main')