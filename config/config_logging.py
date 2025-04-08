import os
import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logging():
    """
    Sets up logging for the application.

    Creates a log file in the 'logs' directory with the current date as the filename.
    Logs are written to both a file and the console.
    """
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_filename = os.path.join(log_directory, "log")
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    log_level = logging.INFO

    # Create root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Avoid adding multiple handlers if already configured
    if not logger.handlers:
        # Add timed rotating file handler
        file_handler = TimedRotatingFileHandler(log_filename, when="midnight", backupCount=14)
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)

        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(console_handler)

    return logging.getLogger(__name__)