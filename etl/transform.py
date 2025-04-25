from helpers.utils import cast_currency_cols_to_numeric, clean_address

def transform_data(file, df):
    """
    Transforms the given DataFrame based on the filename.

    This function applies various transformations to the DataFrame such as
    casting currency columns to numeric, filling missing values, cleaning
    addresses, and formatting station numbers.

    Args:
        file (str): The name of the file being processed.
        df (pandas.DataFrame): The DataFrame to be transformed.

    Returns:
        tuple: A tuple containing the transformed table name and DataFrame.
    """
    if file == '2024 Loss.xlsx' or file == '2023 Loss.xlsx':
        df = cast_currency_cols_to_numeric(df, ['PRE-INCIDENT PROPERTY', 'PRE-INCIDENT CONTENTS', 'PRE-INCIDENT TOTAL', 'PROP. LOSS', 'CONT. LOSS', 'TOTAL'])

    # Set tablename to be filename
    tablename = file.split('.')[0].replace(' ', '_')

    if tablename == 'Separated_Employees_Within_30_Days':
        df.columns = df.iloc[2]
        df = df.drop([0, 1, 2]).reset_index(drop=True)
        df = df.dropna(axis=1, how='all')

    if tablename == 'BATS-YTD':
        df['Case Status'] = df['Case Status'].fillna('Investigation Open')

    if 'Address' in df.columns:
        df['Address'] = df['Address'].apply(clean_address)

    # Validate and clean 'StationNumber' columns to be in the format 'Company X'
    if 'StationNumber' in df.columns:
        df['StationNumber'] = df['StationNumber'].apply(
            lambda x: f"Company {int(x)}" if isinstance(x, (int, float)) or str(x).isdigit() else x
        )

    return tablename, df