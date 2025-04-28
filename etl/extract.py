import pandas as pd
from config.config_logging import setup_logging

logger = setup_logging()

def extract_data(filepath):
    """
    Extracts data from a given Excel file path.

    Args:
        filepath (str): Path to the Excel file

    Returns:
        pandas.DataFrame: DataFrame containing the extracted data
    """
    try:
        if filepath.endswith('.xlsx'):
            if filepath == '2024 Loss.xlsx':
                df = pd.read_excel(filepath, sheet_name='2024') # Grab the second sheet name
            else:
                df = pd.read_excel(filepath)
        return df
    except Exception as e:
        logger.error(f"Error in extract_data: {e}", exc_info=True)
        raise