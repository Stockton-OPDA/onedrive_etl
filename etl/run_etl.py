from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data
import logging
from helpers.sql_helpers import connect_db
from config.config import load_config
from pathlib import Path

logger = logging.getLogger(__name__)
cfg = load_config()

SQL_SERVER = cfg.creds.SQL_SERVER
DATABASE = cfg.creds.DATABASE
USERNAME = cfg.creds.USERNAME_SQL
PASSWORD = cfg.creds.PASSWORD_SQL
DRIVER = 'ODBC Driver 17 for SQL Server'

def run_etl(filename, filepath):
    """
    Executes the ETL process for a given file.

    This function connects to the SQL database, extracts data from the specified file,
    transforms the data, and loads it into the database. It handles any exceptions 
    that occur during the process and logs appropriate error messages.

    Args:
        filename (str): The name of the file being processed.
        filepath (str): The path to the file being processed.
    """
    try:
        file_path = Path(filepath)
        department = file_path.parent.name

        engine = connect_db(DRIVER, SQL_SERVER, DATABASE, USERNAME, PASSWORD)
        df = extract_data(filepath)
        if not df.empty:
            tablename, transformed_df = transform_data(filename, df)
            load_data(transformed_df, tablename, engine, department)

    except Exception as e:
        logger.error(f'Error in running {filename} in run_etl.py: {e}', exc_info=True)