import pandas as pd

def cast_currency_cols_to_numeric(df, columns):
    '''
    Cast currency columns to numeric
    
    Args:
        df (pandas.DataFrame): DataFrame to convert
        columns (list): List of columns to convert
    Returns:
        df (pandas.DataFrame): pandas.DataFrame
    
    '''
    for col in columns:
        df[col] = pd.to_numeric(df[col].str.replace('[$,]', '', regex=True))
    return df

def clean_address(address):
    """
    Cleans the given address string by removing unwanted characters.

    Args:
        address (str): The address string to be cleaned.

    Returns:
        str: The cleaned address string with carriage returns, extra whitespace, 
        and leading/trailing whitespace removed.
    """
    cleaned_address = address.replace('_x000D_', '')  # Remove the carriage return
    cleaned_address = ' '.join(cleaned_address.split())  # Remove extra whitespace
    return cleaned_address.strip()  # Remove leading/trailing whitespace