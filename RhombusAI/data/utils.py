import pandas as pd
import numpy as np

def is_category(col: pd.Series, max_unique_ratio=0.5):
    series = col.dropna()
    if len(series) > 0:  # Check if series is not empty
        unique_ratio = len(series.unique()) / len(series)
        if unique_ratio <= max_unique_ratio:  # Check if unique value ratio is below or equal to the threshold
            return True
    return False


def is_complex(col: pd.Series):
    try:
        for value in col.dropna():
            complex(value)  # Attempt to convert each value to complex
    except (ValueError, TypeError):
        return False
    return True

def infer_and_convert_data_types(df):
    for col in df.columns:
        original_col_data = df[col]

       # Handle numeric types, accounting for placeholders like 'Not Available'
        if df[col].dtype == object:
            converted_col = pd.to_numeric(df[col], errors='coerce')
            if converted_col.notna().any():  # If there are any numeric values
                df[col] = converted_col
                # Downcast to appropriate numeric type
                if df[col].dtype == 'float':
                    df[col] = pd.to_numeric(df[col], downcast='float')
                elif df[col].dtype == 'int':
                    df[col] = pd.to_numeric(df[col], downcast='integer')
            else:
                df[col] = original_col_data  # Revert for further analysis

        # Date conversion
        if df[col].dtype == object:
            converted_col = pd.to_datetime(df[col], errors='coerce')
            if converted_col.notna().any():
                df[col] = converted_col
            else:
                df[col] = original_col_data
        
        # Timedelta conversion
        if df[col].dtype == object:
            converted_col = pd.to_timedelta(df[col], errors='coerce')
            if converted_col.notna().any():
                df[col] = converted_col
            else:
                df[col] = original_col_data

        # Boolean conversion
        if df[col].dtype == object:
            if all(val.lower() in ['true', 'false'] for val in df[col].astype(str).str.lower()):
                df[col] = df[col].astype(bool)
        
        # Check for complex numbers
        if df[col].dtype == object:
            if is_complex(df[col]):
                df[col] = df[col].apply(lambda x: complex(x) if pd.notna(x) else x)

        # Categorical data detection using the is_category function
        if df[col].dtype == object:
            if is_category(df[col]):
                df[col] = df[col].astype('category')

    return df

def override_data_type(df, column_name, new_data_type):
    """
    Attempts to convert the data type of a specified column in a DataFrame.

    Parameters:
    - df: pandas.DataFrame - The DataFrame containing the data.
    - column_name: str - The name of the column to convert.
    - new_data_type: str - The desired new data type (e.g., 'int', 'float', 'str', 'bool', 'datetime64', 'timedelta64', 'category', 'complex').

    Returns:
    - pandas.DataFrame: The DataFrame with the specified column's data type converted.
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    
    original_col_data = df[column_name].copy()

    try:
        if new_data_type == 'complex':
            df[column_name] = df[column_name].apply(lambda x: complex(x) if pd.notna(x) else x)
        elif new_data_type == 'category':
            df[column_name] = df[column_name].astype('category')
        elif new_data_type in ['int', 'float', 'bool', 'str']:
            df[column_name] = df[column_name].astype(new_data_type)
        elif new_data_type == 'datetime64':
            df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
        elif new_data_type == 'timedelta64':
            df[column_name] = pd.to_timedelta(df[column_name], errors='coerce')
        else:
            raise ValueError(f"Unsupported data type: {new_data_type}")
    except (ValueError, TypeError):
        print(f"Conversion to {new_data_type} failed for column '{column_name}'. Reverting to original data.")
        df[column_name] = original_col_data

    return df

# Test the function with your DataFrame
# df = pd.read_csv('sample_data.csv')
# print("Data types before inference:")
# print(df.dtypes)

# df = infer_and_convert_data_types(df)

# print("\nData types after inference:")
# print(df.dtypes)

# %%