# OneDrive - SQL File Synchronization Service

This project automates data synchronization between various departmental OneDrive folders to the OPDA on-premise SQL server for use in PowerBI / STAT. 

This project uses a RabbitMQ-based messaging system consisting of a producer and a consumer. The producer monitors file creation or modification events for subfolders within a specified directory, while the consumer processes the messages sent to the RabbitMQ queue.

Currently, the following departments are monitored:
  - CDD
  - EDD
  - FD
  - HR
  - PD
  - PW
  - OVP

## Features

- **Producer**:
  - Monitors a directory for file changes using the `watchdog` library.
  - Sends JSON messages to a RabbitMQ queue upon detecting file events.
  - Handles RabbitMQ connection errors with a retry mechanism for recovery.

- **Consumer**:
  - Consumes messages from the RabbitMQ queue.
  - Processes the messages based on your custom business logic.
  - Includes connection recovery to handle network or RabbitMQ failures.

- **Resilience**:
  - Automatic reconnection and retry mechanism for both producer and consumer.
  - Graceful handling of shutdown signals (e.g., `KeyboardInterrupt`).

## Installation

1. **Clone the repository:**

   ```
   git clone https://github.com/Stockton-OPDA/onedrive_etl.git
   cd rabbitmq-service
   ```

2. **Set up a virtual environment:**

   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```
   pip install -r requirements.txt
   ```

4. **Configure RabbitMQ credentials:**
   
   Update the `config.yaml` file in the `config` folder with your own credentials:
   ```
   creds:
     SQL_SERVER: '<SQL_SERVER_HOSTNAME>'
     DATABASE: '<DATABASE_NAME>'
     USERNAME_SQL: '<SQL_USERNAME>'
     PASSWORD_SQL: '<SQL_PASSWORD>'
   RABBITMQ_SETTINGS:
     host: '<RABBITMQ_HOST>'
     port: <RABBITMQ_PORT>
     username: '<RABBITMQ_USERNAME>'
     password: '<RABBITMQ_PASSWORD>'
   ONEDRIVE:
     PATH: '<ONEDRIVE_PATH>'
     SUBFOLDERS: ['CDD', 'EDD', 'FD', 'HR', 'PD', 'PW', 'OVP']
   ```

## Configuration

### RabbitMQ Settings

Update the following settings in `config/config.yaml`:

- `rabbitmq_host`: The hostname of the RabbitMQ server.
- `rabbitmq_port`: The port number for RabbitMQ (default: 5672).
- `rabbitmq_user`: The username for RabbitMQ authentication.
- `rabbitmq_password`: The password for RabbitMQ authentication.
- `rabbitmq_queue`: The queue name used for messaging.

### Directory Monitoring

Specify the directory to monitor for file changes in the `ONEDRIVE_PATH` constant in `messaging/producer.py`.

## Usage

### Start the Producer and Consumer

Run the batch file `run.bat`.

NOTE: Ensure that you do NOT click into the command prompt window. This will cause the application to freeze and will block the application from operating as normal. You will know the application is frozen if the command prompt window shows "Select" in front of the window title. 

Run the following commands to start the producer and consumer processes:
   ```
   python main.py
   ```

This will:

- Start the producer process to monitor the specified directory.
- Start the consumer process to listen for and process messages from RabbitMQ.

Alternatively, you can run the program from the included `run.bat` file.

### Stopping the Services

Press `Ctrl+C` to gracefully stop both the producer and consumer processes.

## Code Structure

- **main.py**:
  - Entry point for the application. Starts both producer and consumer processes using `multiprocessing`.

- **messaging/producer.py**:
  - Implements the producer logic, including directory monitoring and message publishing.

- **messaging/consumer.py**:
  - Implements the consumer logic, including message consumption and processing.

- **messaging/rabbitmq_connector.py**:
  - Contains the `connect_to_broker` function for creating RabbitMQ connections and channels.

- **config/config.py**:
  - Provides functions to load application configuration from `config.yaml`.

- **config/config_logging.py**:
  - Sets up application-wide logging.

## Error Handling and Recovery

- Both producer and consumer processes use a retry mechanism to recover from RabbitMQ connection errors.
- If a connection is lost, the application retries with a delay and uses an exponential backoff strategy to avoid rapid reconnection attempts.
- Graceful shutdown ensures proper resource cleanup (e.g., closing RabbitMQ channels and connections).

## Requirements

- Python 3.8+
- RabbitMQ server

## Logging

Logs are stored in the `/logs` directory as specified in the `config.yaml` file. The logging configuration can be customized in `config/config_logging.py`. The logs are rotated daily at midnight.


## License
As a work of the City of Stockton, this project is in the public domain within the United States.

Additionally, we waive copyright and related rights of the work worldwide through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/deed.en).
