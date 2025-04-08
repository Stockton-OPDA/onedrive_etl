import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from helpers.sql_helpers import connect_db
from config.config import load_config
import logging
import os
import pika
import json
from datetime import datetime
from messaging.rabbitmq_connector import connect_to_broker

logger = logging.getLogger(__name__)
cfg = load_config()

QUEUE_NAME = 'file_events'
ONEDRIVE_PATH = cfg.ONEDRIVE_PATH
SQL_SERVER = cfg.creds.SQL_SERVER
DATABASE = cfg.creds.DATABASE
USERNAME = cfg.creds.USERNAME_SQL
PASSWORD = cfg.creds.PASSWORD_SQL
DRIVER = 'ODBC Driver 17 for SQL Server'

engine = connect_db(DRIVER, SQL_SERVER, DATABASE, USERNAME, PASSWORD)

class Publisher(FileSystemEventHandler):
    def __init__(self):
        """ Initializes the Publisher class. Debounces messages by 5 seconds. """
        super().__init__()
        self.last_message_sent = {}
        self.DEBOUNCE_TIME = 5
        self.connection, self.channel = connect_to_broker()

    def send_message(self, filepath, event_type):
        """
        Sends a message to the RabbitMQ queue if the time since the last
        message sent for the same filepath is greater than or equal to
        self.DEBOUNCE_TIME.

        Parameters:
            filepath (str): The path of the file that triggered the event.
            event_type (str): The type of event that triggered the message (e.g. "created", "modified", etc.).
        """
        current_time = time.time()
        last_messaged_time = self.last_message_sent.get(filepath, 0)
        if current_time - last_messaged_time >= self.DEBOUNCE_TIME:
            filename = os.path.basename(filepath)
            message = {
                "filename": filename,
                "filepath": filepath,
                "event_type": event_type,
                "timestamp": datetime.now().isoformat()
            }

            # Ensure connection is still active
            self.connection, self.channel = connect_to_broker()

            # Publish message to queue
            self.channel.basic_publish(
                exchange='',
                routing_key=QUEUE_NAME,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2  # Make the message persistent
                )
            )
            print(f"File: {filename} {event_type}, JSON message sent to queue.")
            logger.info(f'File: {filename} {event_type}, JSON message sent to queue.')
            self.last_message_sent[filepath] = current_time

    def on_modified(self, event):
        """
        Triggered when a file or directory is modified.

        Args:
            event (watchdog.events.FileSystemEvent): The event that triggered the callback.
        """
        if not event.is_directory:
            self.send_message(event.src_path, "modified")

    def on_created(self, event):
        """
        Triggered when a file or directory is created.

        Args:
            event (watchdog.events.FileSystemEvent): The event that triggered the callback.
        """
        if not event.is_directory:
            self.send_message(event.src_path, "created")

def run_producer():
    """
    Initializes and starts a watchdog service to monitor file creation 
    or modification events in a specified directory. JSON messages are 
    sent to a RabbitMQ queue.
    """
    try:
        print("Starting the producer...")
        logger.info("Starting the producer...")

        # Create observer and event handler
        observer = Observer()
        publisher = Publisher()
        observer.schedule(publisher, ONEDRIVE_PATH, recursive=False)
        observer.start()

        print(f"Monitoring started in {ONEDRIVE_PATH} for file changes...")
        logger.info(f"Monitoring started in {ONEDRIVE_PATH} for file changes...")

        while True:
            time.sleep(5) # Keep process alive to detect file changes

    except KeyboardInterrupt:
        observer.stop()
        print("Monitoring stopped.")
        logger.info("Monitoring stopped.")
        publisher.channel.close()
        publisher.connection.close()
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Producer connection error: {e}, retrying...")
        logger.warning(f"Producer connection error: {e}, retrying...")
        time.sleep(5)  # Retry after delay
    except Exception as e:
        print(f"Producer error: {e}, retrying...")
        logger.error(f"Producer error: {e}, retrying...")
        time.sleep(5)

def main():
    run_producer()


if __name__ == "__main__":
    main()