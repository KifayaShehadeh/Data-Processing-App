import re
import pandas as pd
import numpy as np
import traceback
from dateutil import parser
from dateutil.parser import ParserError
from .conversions import is_allowed_none, convert_to_boolean, convert_to_categorical, convert_to_datetime, convert_to_numeric, convert_to_timedelta, convert_to_complex, looks_like_number
from .typechecks import is_category, is_complex, is_timedelta, looks_like_currency, looks_like_number
from .data_handling import normalise_boolean, parse_mixed_data, can_parse_date, preprocess_for_float_conversion
from django.db.models import Max
from .models import Dataset, ColumnType
from django.db.models import Max

column_type_overrides = {}

def infer_data_type(col):
    """
    Infers the most likely data type of a given pandas Series by analyzing its contents.

    The function checks for specific patterns and types within the series, such as boolean values,
    complex numbers, numeric values, currencies, time durations, dates, categories, and textual data.
    It preprocesses the data to normalize boolean values and clean numeric and textual representations.

    Parameters:
    - col (pd.Series): A pandas Series whose data type is to be inferred.

    Returns:
    - str: A string representing the inferred data type, such as 'Boolean', 'Decimal', 'Date', etc.
    """
    # Preprocess column, removing commas and converting to None types as needed
    col_normalised_bool = col.apply(normalise_boolean)
    if pd.api.types.is_bool_dtype(col_normalised_bool):
        return 'Boolean'
    
    col_cleaned = col.apply(lambda x: x.replace(',', '').strip() if isinstance(x, str) else x)
    col_cleaned = col_cleaned.apply(lambda x: None if is_allowed_none(x) else x)

    print(f"Cleaned {col.name}:", col_cleaned.tolist())  # Debug print statement
    if all(isinstance(x, bool) for x in col_cleaned.dropna()):
        return 'Boolean'
    if any(is_complex(x) for x in col_cleaned.dropna()):
        return 'Complex Number'
    if all(looks_like_number(x) for x in col_cleaned.dropna()):
        return 'Decimal'
    if all(looks_like_currency(x) for x in col_cleaned.dropna()):
        return 'Decimal'
    if any(is_timedelta(str(x)) for x in col.dropna()):
        return 'Time Duration'
    if any(can_parse_date(str(x)) for x in col.dropna()):
        return 'Date'
    if len(set(col.dropna())) < len(col.dropna()) / 2:
        return 'Category'
    if all(isinstance(x, str) for x in col.dropna()):
        return 'Text'

    return 'Text'



def infer_and_convert_data_types(df):
    """
    Iterates through each column of a DataFrame, infers its data type, and converts it to a more
    specific type where applicable. This can help in optimizing memory usage and ensuring data
    integrity by enforcing consistent data types across the DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame whose columns are to be analyzed and converted.

    Returns:
    - pd.DataFrame: The same DataFrame with its columns converted to the inferred data types.
    """
    for col in df.columns:
        dtype = infer_data_type(df[col])
        if dtype == 'Decimal':
            df[col] = convert_to_numeric(df, col)
        elif dtype == 'Date':
            df[col] = convert_to_datetime(df, col)
        elif dtype == 'Time Duration':
            df[col] = convert_to_timedelta(df, col)
        elif dtype == 'Complex Number':
            df[col] = convert_to_complex(df, col)
        elif dtype == 'Boolean':
            df[col] = convert_to_boolean(df, col)
        elif dtype == 'Category':
            df[col] = df[col].astype('category')
    
    return df

def get_user_friendly_dtype(dtype):
    """
    Converts a pandas data type object into a more user-friendly string representation that is easier
    to understand and work with in a data processing context.

    Parameters:
    - dtype: A pandas dtype object or a string that represents a dtype.

    Returns:
    - str: A user-friendly string representation of the input data type, such as 'Integer', 'Decimal',
    'Complex Number', 'Time Duration', 'Boolean', 'Date', 'Category', or 'Text'.
    """
    dtype_name = str(dtype)
    if dtype_name.startswith('int') or dtype_name.startswith('uint'):
        return 'Integer'
    elif dtype_name.startswith('float'):
        return 'Decimal'
    elif dtype_name.startswith('complex'):
        return 'Complex Number'
    elif dtype_name.startswith('timedelta'):
        return 'Time Duration'
    else:
        return {
            'object': 'Text',
            'bool': 'Boolean',
            'datetime64[ns]': 'Date',
            'category': 'Category',
        }.get(dtype_name, dtype_name)  # Default to original if no match found
    
def serialise_dataframe(df):
    """
    Converts a pandas DataFrame into a list of dictionaries, with special handling to ensure all
    data types are properly converted to formats suitable for JSON serialization. This includes
    converting date and time types to strings, handling NaN and NaT values, and ensuring categorical
    data is represented accurately.

    Parameters:
    - df (pd.DataFrame): The DataFrame to serialize.

    Returns:
    - list: A list of dictionaries, each representing a row in the DataFrame, ready for JSON serialization.
    """
    df = df.copy()
    for column in df.columns:
        dtype = df[column].dtype
        if pd.api.types.is_datetime64_any_dtype(dtype):
            df[column] = df[column].dt.strftime('%Y-%m-%d %H:%M:%S').replace(pd.NaT, "N/A")
        elif pd.api.types.is_timedelta64_dtype(dtype):
            df[column] = df[column].apply(lambda x: x.total_seconds() if pd.notnull(x) else "N/A")
        elif pd.api.types.is_categorical_dtype(dtype) or pd.api.types.is_object_dtype(dtype):
            df[column] = df[column].astype(str).replace({'nan': "N/A", 'None': "N/A"})
        elif pd.api.types.is_complex_dtype(dtype):
            df[column] = df[column].apply(lambda x: str(x) if pd.notnull(x) else "N/A")

        else:
            # Convert NaN values to None, which will be serialised as null in JSON
            df[column] = df[column].apply(lambda x: 'N/A' if pd.isnull(x) else x)
    
    return df.to_dict(orient='records')

def override_data(df, column, new_type):
    """
    Attempts to explicitly convert the data type of a specified column in a DataFrame to a new
    specified type. This can be useful for data cleaning and preparation, especially if the
    initial data type inference was incorrect or suboptimal.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the column to be converted.
    - column (str): The name of the column whose data type is to be overridden.
    - new_type (str): The target data type to convert the column to.

    Returns:
    - tuple: A tuple containing a boolean indicating whether the conversion was successful, and a
             string message with details about the conversion outcome.
    """
    print(f"Attempting to override column '{column}' to new type '{new_type}'.")
    try:
        conversion_functions = {
            'Date': lambda col: convert_to_datetime(df, col),
            'Integer': lambda col: pd.to_numeric(df[col], errors='raise').astype('Int64'),
            'Decimal': lambda col: convert_to_numeric(df, col),  # Using convert_to_numeric for Decimal as well
            'Time Duration': lambda col: pd.to_timedelta(df[col], errors='raise'),
            'Boolean': lambda col: convert_to_boolean(df, col),
            'Complex Number': lambda col: df[col].apply(lambda x: complex(x) if pd.notna(x) else x),
            'Category': lambda col: convert_to_categorical(df, col, is_category),  # Note: Ensure you have an is_category function defined
            'Text': lambda col: df[col].astype(str)
        }

        if new_type in conversion_functions:
            # Check if all values can be converted without error
            if can_convert(column, conversion_functions[new_type]):
                df[column] = conversion_functions[new_type](column)
                global column_type_overrides
                column_type_overrides[column] = new_type
                return True, f"Data type overridden successfully to {new_type}."
            else:
                return False, f"Cannot convert from {column} to {new_type}, operation aborted."
        else:
            return False, f"Invalid data type specified: {new_type}."

    except Exception as e:
        traceback_str = traceback.format_exc()
        print(traceback_str)
        return False, str(e)
    
def can_convert(col, conversion_function):
    """
    Checks if the values in a pandas Series can be converted using a given conversion function without raising an error.

    Parameters:
    - col (pd.Series): The pandas Series to check.
    - conversion_function (callable): The function to use for attempting the conversion.

    Returns:
    - bool: True if the conversion can be performed without errors, False otherwise.
    """
    try:
        # Attempt conversion
        conversion_function(col)
        return True
    except:
        return False
