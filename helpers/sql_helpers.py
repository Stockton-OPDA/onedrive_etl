import pandas as pd
import sqlalchemy
import urllib
from sqlalchemy.engine.base import Engine
from sqlalchemy import Integer, String, Float, DateTime, text
from sqlalchemy.types import Integer, String, Float, DateTime
from config.config_logging import setup_logging

logger = setup_logging()

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

def infer_sql_dtype(column_name: str, dtype: str):
    """
    Infers the SQLAlchemy type based on the column name and Pandas dtype.

    Args:
        column_name (str): The name of the column.
        dtype (str): The Pandas dtype of the column.

    Returns:
        sqlalchemy.types.TypeDecorator: The inferred SQLAlchemy type.
    """
    if "date" in column_name.lower():
        return DateTime()
    elif dtype == 'int64':
        return Integer()
    elif dtype == 'float64':
        return Float()
    else:
        return String()

def upload_dataframe_to_sql(df: pd.DataFrame, table_name: str, engine: Engine, schema: str, append_or_replace: str = 'replace') -> None:
    """
    Uploads a DataFrame to a SQL Server database table. If the table already exists, it is dropped and re-created with the DataFrame data.
    Creates the schema if it does not exist.

    Args:
        df (pandas.DataFrame): The DataFrame to be uploaded.
        table_name (str): The name of the table in the SQL database.
        engine (sqlalchemy.engine.base.Engine): The SQLAlchemy engine connected to the database.
        schema (str): The name of the schema in the SQL database.
        append_or_replace (str, optional): The action to take when the table already exists. Defaults to 'replace'.
    """
    if df.empty:
        logger.warning(f"The DataFrame for table {table_name} is empty. Skipping upload.")
        return

    try:
        with engine.connect() as conn:
            with conn.begin():
                check_schema_exists = text(f"""
                    SELECT 1 FROM sys.schemas WHERE name = :schema
                """)
                result = conn.execute(check_schema_exists, {'schema': schema}).scalar()

                if not result:
                    create_schema = text(f"EXEC('CREATE SCHEMA {schema}')")
                    conn.execute(create_schema)
                    logger.info(f"New schema '{schema}' created.")

                # Upload DataFrame
                df.to_sql(table_name, conn, if_exists=append_or_replace, index=False, schema=schema)
                logger.info(f"Table {schema}.{table_name} created and data uploaded.")

    except Exception as e:
        logger.error(f"Error in upload_dataframe_to_sql with {schema}.{table_name}: {e}")