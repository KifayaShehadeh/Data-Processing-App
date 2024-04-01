import re
import pandas as pd
import numpy as np
import traceback
from dateutil import parser
from dateutil.parser import ParserError
from .conversions import is_allowed_none

def normalise_boolean(val):
    """
    Normalizes boolean values represented as strings to Python booleans.

    Parameters:
    - val (str or any): The value to normalize.

    Returns:
    - bool or pd.NA: The normalized boolean value, or pd.NA if unconvertible.
    """
    true_values = ['true', '1', 'yes', 't', 'on']
    false_values = ['false', '0', 'no', 'f', 'off']
    if str(val).lower() in true_values:
        return True
    elif str(val).lower() in false_values:
        return False
    else:
        return pd.NA  # Use pandas NA for undefined or unconvertible values


def parse_mixed_data(col):
    """
    Determines the types of data present in a column of mixed data types.

    Parameters:
    - col (iterable): The column containing mixed data types.

    Returns:
    - set: A set of unique data types found in the column ('number', 'date', 'string').
    """
    # Check if there are different types of data in the column (excluding allowed none types)
    unique_types = set()
    for val in col:
        if is_allowed_none(val) or pd.isna(val):
            continue
        try:
            # Attempt to parse as float to see if the value is numeric
            # Only strip commas if the value is a string
            if isinstance(val, str):
                float(val.replace(",", "").strip())
            else:
                float(val)
            unique_types.add('number')
        except ValueError:
            try:
                # If the value can be parsed as a date, then consider it as a date
                parser.parse(str(val))
                unique_types.add('date')
            except (ValueError, TypeError):
                # If it's neither, consider it as a string
                unique_types.add('string')
    return unique_types


def can_parse_date(string):
    """
    Checks if a string can be parsed as a date, excluding patterns that are not dates.

    Parameters:
    
    string (str): The string to check for date validity.

        Returns:
        
    bool: True if the string can be parsed as a date, False otherwise."""
    # Define non-date patterns to exclude strings that shouldn't be considered as dates
    non_date_patterns = [
        r"^\d+$",  # Strings that are only digits are not dates
        r"^-?\d+(.\d+)?$",  # Strings that represent a float number are not dates
    ]
    # Check against non-date patterns before attempting to parse
    if any(re.search(pattern, string) for pattern in non_date_patterns):
        return False
    try:# Attempt to parse the string as a date without using fuzzy logic
        parsed_date = parser.parse(string, fuzzy=False)
        # Additional check to ensure the string represents a meaningful date# For instance, ensuring the year makes sense (you might adjust this range)
        if parsed_date.year >= 1000 and parsed_date.year <= 9999:
            return True
        else:
            return False
    except (parser.ParserError, TypeError, ValueError):# If parsing fails, the string is not a date
        return False

def preprocess_for_float_conversion(col):
    """
    Preprocesses a pandas Series for float conversion by replacing non-convertible values with NaN.

    Parameters:
    - col (pd.Series): The pandas Series to preprocess.

    Returns:
    - pd.Series: The preprocessed Series ready for float conversion.
    """
    col = pd.to_numeric(col, errors='coerce')
    return col


