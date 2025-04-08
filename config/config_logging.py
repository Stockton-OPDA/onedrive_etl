import os
import logging
from datetime import datetime

def setup_logging():
    """
    Sets up logging for the application.

    Creates a log file in the 'logs' directory with the current date as the filename.
    The logging level is set to INFO and the log format is set to include the timestamp, log level, and message.

    Returns a logger object with the name of the current module.
    """    
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_filename = os.path.join(log_directory, datetime.now().strftime("log_%Y-%m-%d.log"))
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    return logging.getLogger(__name__)