import pandas as pd

def extract_data(filepath):
    """
    Extracts data from a given Excel file path.

    Args:
        filepath (str): Path to the Excel file

    Returns:
        pandas.DataFrame: DataFrame containing the extracted data
    """
    if filepath.endswith('.xlsx'):
        if filepath == '2024 Loss.xlsx':
            df = pd.read_excel(filepath, sheet_name='2024') # Grab the second sheet name
        else:
            df = pd.read_excel(filepath)
    return df