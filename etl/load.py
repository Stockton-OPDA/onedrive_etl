from helpers.sql_helpers import upload_dataframe_to_sql
import logging

logger = logging.getLogger(__name__)

def load_data(df, tablename, engine, schema):
    """
    Loads a DataFrame into a specified SQL database table.

    This function uploads a given DataFrame to a SQL table using the provided 
    SQLAlchemy engine. The table is created or replaced in the specified schema.

    Args:
        df (pandas.DataFrame): The DataFrame to be uploaded.
        tablename (str): The name of the table in the SQL database.
        engine (sqlalchemy.engine.base.Engine): The SQLAlchemy engine connected to the database.
        schema (str): The schema for the table, named after the department that the file is from.

    Notes:
        - If the table already exists, it is replaced with the new data.
    """
    try:
        upload_dataframe_to_sql(df, tablename, engine, schema)
        logger.info(f"Data uploaded to SQL table: {tablename}")
    except Exception as e:
        logger.error(f"Error in upload_dataframe_to_sql with {tablename}: {e}", exc_info=True)