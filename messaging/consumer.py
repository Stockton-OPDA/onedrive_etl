import pika
import json
from etl.run_etl import run_etl
from config.config import load_config
from messaging.rabbitmq_connector import connect_to_broker
import logging
import time

logger = logging.getLogger(__name__)
cfg = load_config()

QUEUE_NAME = 'file_events'

def on_message(channel, method, properties, body):
    """
    Callback function for consuming from RabbitMQ queue.

    This function is called whenever a message is received from the queue. It
    extracts the filename, filepath, event type and timestamp from the message
    and calls the run_etl function to process the file.

    Args:
        channel (pika.channel.Channel): The RabbitMQ channel object.
        method (pika.spec.Basic.Deliver): The RabbitMQ method object.
        properties (pika.spec.BasicProperties): The RabbitMQ message properties.
        body (bytes): The message body as a bytes object.
    """
    message = json.loads(body)
    filename = message.get("filename")
    filepath = message.get("filepath")
    event_type = message.get("event_type")
    timestamp = message.get("timestamp")

    logger.info(f"Received file: {filename} from queue - Event: {event_type}, Time: {timestamp}")
    run_etl(filename, filepath)

def run_consumer():
    """
    Initializes and starts a RabbitMQ consumer to consume JSON messages from the designated OneDrive queue.
    """
    while True:
        try:
            logger.info("Starting the consumer...")
            connection, channel = connect_to_broker()
            channel.queue_declare(queue=QUEUE_NAME, durable=True)
            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message, auto_ack=True)
            
            logger.info("Waiting for JSON messages...")

            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            logger.warning(f"Consumer connection error: {e}, retrying...")
            time.sleep(5)
            continue
        except Exception as e:
            logger.error(f"Consumer error: {e}, retrying...")
            time.sleep(5)

def main():
    """Main entry point for the script with retry mechanism."""
    while True:
        try:
            logger.info("Connecting to RabbitMQ...")
            run_consumer()
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Connection error: {e}. Retrying in 5 seconds...", exc_info=True)
            time.sleep(5)
        except KeyboardInterrupt:
            logger.info("User interrupt, shutting down queue...")
            break 
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            break

if __name__ == "__main__":
    main()