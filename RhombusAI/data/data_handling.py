import re
import pandas as pd
import numpy as np
import traceback
from dateutil import parser
from dateutil.parser import ParserError
from .conversions import is_allowed_none

def normalise_boolean(val):
    true_values = ['true', '1', 'yes', 't', 'on']
    false_values = ['false', '0', 'no', 'f', 'off']
    if str(val).lower() in true_values:
        return True
    elif str(val).lower() in false_values:
        return False
    else:
        return pd.NA  # Use pandas NA for undefined or unconvertible values

    

def parse_mixed_data(col):
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
    try:
        # Attempt to parse the string as a date.
        result = parser.parse(string, fuzzy=False)
        
        # Check if the result is really a date by ensuring it doesn't match certain non-date patterns
        non_date_patterns = [
            r"^\d+$",  # Strings that are only digits are not dates.
            r"[a-zA-Z]",  # Strings containing letters that were not parsed into a month name are not dates.
            r"^-?\d+(\.\d+)?$",  # Strings that represent a float number are not dates.
            # Add any more patterns that are known to be not dates.
        ]
        if any(re.search(pattern, string) for pattern in non_date_patterns):
            return False
        # If the date was parsed without fuzzy logic, it is likely a valid date.
        return True
    except (parser.ParserError, TypeError, ValueError):
        # If the parsing fails, it's not a date.
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


