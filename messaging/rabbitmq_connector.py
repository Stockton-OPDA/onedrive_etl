import pika
import pika.exceptions
from config.config import load_config
import time
from config.config_logging import setup_logging

logger = setup_logging()

cfg = load_config()

def connect_to_broker(max_retries=5):
    """
    Attempts to connect to RabbitMQ with retries.

    Args:
        max_retries: Maximum retry attempts (-1 for infinite retries)
    
    Returns:
        connection: Established connection
        channel: The channel connection

    Raises:
        Exception if connection fails after max_retries
    """
    attempts = 0
    while max_retries == -1 or attempts < max_retries:
        try:
            credentials = pika.PlainCredentials(cfg.RABBITMQ_SETTINGS.username, cfg.RABBITMQ_SETTINGS.password)
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
            channel = connection.channel()
            print("Connected to RabbitMQ.")
            logger.info("Connected to RabbitMQ.")
            return connection, channel
        except pika.exceptions.AMQPConnectionError:
            attempts += 1
            delay = min(2 ** attempts, 30) # Exponential backoff with max delay of 30 seconds
            print(f"Connection failed, retrying in {delay} seconds...")
            logger.warning(f"Connection failed, retrying in {delay} seconds...")
            time.sleep(delay)
    raise Exception(f"Failed to connect to RabbitMQ after {attempts} attempts")