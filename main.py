from config.config_logging import setup_logging
from config.config import load_config
import time
import multiprocessing
from messaging.producer import run_producer
from messaging.consumer import run_consumer

# Set up logging and config
cfg = load_config()
logger = setup_logging()


if __name__ == "__main__":
    try:
        # Create RabbitMQ processes
        watcher_process = multiprocessing.Process(target=run_producer)
        consumer_process = multiprocessing.Process(target=run_consumer)

        watcher_process.start()
        consumer_process.start()

        # Keep the main program running while the other processes are active
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping processes...")
            watcher_process.terminate()
            consumer_process.terminate()

            watcher_process.join()
            consumer_process.join()
            logger.info("Processes stopped.")

    except Exception as e:
        logger.error(f"An error occurred in main.py: {e}", exc_info=True)