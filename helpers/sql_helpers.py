import pandas as pd
import sqlalchemy
import logging
import urllib
from sqlalchemy.engine.base import Engine

logger = logging.getLogger(__name__)

def connect_db(DRIVER: str, SERVER: str, DATABASE: str, USERNAME: str, PASSWORD: str) -> Engine:
    """
    Establishes a connection to a SQL Server database using the provided credentials.

    This function creates and returns an SQLAlchemy engine for connecting to a SQL Server database. 
    The connection string is constructed using the provided driver, server, database, username, and password.

    Args:
        DRIVER (str): The ODBC driver to use for the connection.
        SERVER (str): The name or IP address of the SQL Server.
        DATABASE (str): The name of the database to connect to.
        USERNAME (str): The username for authentication.
        PASSWORD (str): The password for authentication.

    Returns:
        Engine: The SQLAlchemy engine connected to the SQL Server.

    Raises:
        ConnectionError: If there is an error in constructing the connection string or creating the engine.
    """
    try:
        # Construct the connection string
        params = urllib.parse.quote_plus(
            f'Driver={DRIVER};'
            f'Server={SERVER};'
            f'Database={DATABASE};'
            f'Uid={USERNAME};'
            f'Pwd={PASSWORD};'
            f'Encrypt=yes;'
            f'TrustServerCertificate=yes;'
        )
        conn_str = f'mssql+pyodbc:///?odbc_connect={params}'
        
        # Create the engine
        engine = sqlalchemy.create_engine(conn_str)
        
        # Test the connection
        with engine.connect() as connection:
            logger.info("Connected to SQL Server")
        
        return engine

    except sqlalchemy.exc.SQLAlchemyError as e:
        logger.error("Failed to connect to the database: %s", e)
        raise ConnectionError(f"Failed to connect to the {SERVER} database: {e}")
    
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        raise ConnectionError(f"An unexpected error occurred: {e}")
    
def fetch_sql_data(engine: Engine, query: str) -> pd.DataFrame:
    """
    Fetches data from a SQL Server database using a provided query and returns it as a Pandas DataFrame.

    Args:
        xx

    Returns:
        xx

    Raises:
        xx
    """
    try:
        with engine.connect() as conn:
            trans = conn.begin()
            try:
                df = pd.read_sql(query, conn)
                trans.commit()  # No actual commit needed for SELECT, but this ensures the transaction is completed cleanly
                return df
            except Exception as proc_error:
                trans.rollback()
                logger.error(f"An error occurred during transaction: {proc_error}")
                raise
    except Exception as e:
        logger.error(f"An error occurred while connecting to the database: {e}")
        raise