import re
import pandas as pd
import numpy as np
import traceback
from dateutil import parser
from dateutil.parser import ParserError

def is_timedelta(column):
    """
    Checks if a column contains text representing time durations.

    Parameters:
    - column (pd.Series): The column to check.

    Returns:
    - bool: True if the column contains text representing time durations, False otherwise.
    """
    patterns = [
        r'\d+\s*years?',
        r'\d+\s*months?',
        r'\d+\s*weeks?',
        r'\d+\s*days?',
        r'\d+\s*hours?',
        r'\d+\s*minutes?',
        r'\d+\s*seconds?',
    ]
    
    for pattern in patterns:
        if column.str.contains(pattern, case=False, regex=True).any():
            return True
    
    return False


def is_category(col: pd.Series, max_unique_ratio=0.5):
    """
    Determines if the given pandas Series should be treated as a categorical data type based on its unique value ratio.

    Parameters:
    - col (pd.Series): The pandas Series to analyze.
    - max_unique_ratio (float): The maximum ratio of unique values to total values that allows the Series to be 
      considered categorical. Defaults to 0.5.

    Returns:
    - bool: True if the Series is considered categorical, False otherwise.
    """
    series = col.dropna()
    if len(series) > 0:  # Check if series is not empty
        unique_ratio = len(series.unique()) / len(series)
        if unique_ratio <= max_unique_ratio:  # Check if unique value ratio is below or equal to the threshold
            return True
    return False

def is_complex(col: pd.Series):
    """
    Checks if the given pandas Series contains complex number data.

    Parameters:
    - col (pd.Series): The pandas Series to check.

    Returns:
    - bool: True if the Series contains complex numbers, False otherwise.
    """
    try:
        for value in col.dropna():
            complex(value)  # Attempt to convert each value to complex
    except (ValueError, TypeError):
        return False
    return True


def is_complex(val):
    """
    Determines whether a given value represents a complex number.

    This function checks if the input is either an instance of a complex number or a string that
    represents a complex number in the standard mathematical form (a + bi). The function
    supports strings with or without spaces around the '+' or '-' signs. It also handles cases
    where either the real part (a) or the imaginary part (bi) is omitted.

    Parameters:
    - val (complex, str): The value to be checked. Can be an actual complex number or a string.

    Returns:
    - bool: True if `val` is a complex number or a string that represents a complex number.
            False otherwise.
    """
    if isinstance(val, complex):
        return True
    if isinstance(val, str):
        # Match strings that are in the form of a complex number (a + bi)
        match = re.match(r'^([+-]?[\d.]+)?([+-]?[\d.]+j)$', val.strip().replace(' ', ''))
        return bool(match)
    return False


def is_timedelta(string):
    """
    Checks if a string represents a time duration using common time units.

    This function searches for patterns in the string that indicate time units, such as
    'years', 'months', 'weeks', 'days', 'hours', 'minutes', and 'seconds'. The presence of
    any of these units (with optional pluralization) and a preceding numeric value qualifies
    the string as representing a time duration.

    Parameters:
    - string (str): The string to check for time duration representation.

    Returns:
    - bool: True if the string contains time duration patterns, False otherwise.
    """
    # Patterns for different time units
    patterns = [
        r'\b\d+\s*years?\b',
        r'\b\d+\s*months?\b',
        r'\b\d+\s*weeks?\b',
        r'\b\d+\s*days?\b',
        r'\b\d+\s*hours?\b',
        r'\b\d+\s*minutes?\b',
        r'\b\d+\s*seconds?\b',
    ]
    return any(re.search(pattern, string, re.IGNORECASE) for pattern in patterns)

def looks_like_number(val):
    """
    Determines whether a given value can be interpreted as a number.

    This function checks if the input is a numerical data type (int, float, or np.number) or
    a string that represents a number, potentially with commas as thousands separators or
    a percentage sign at the end. It handles both positive and negative numbers.

    Parameters:
    - val: The value to check. Can be of any type.

    Returns:
    - bool: True if `val` can be interpreted as a numerical value, False otherwise.
    """
    if pd.isna(val):
        return False
    if isinstance(val, (int, float, np.number)):
        return True
    if isinstance(val, str):
        val = val.replace(',', '').strip()
        # Check for a percentage at the end of the string and remove it
        if val.endswith('%'):
            val = val[:-1]
        # This regex will match any string that represents an int or float, negative or positive
        if re.match(r'^-?\d+(?:\.\d+)?$', val):
            return True
    return False

def looks_like_currency(val):
    """
    Determines whether a given value can be interpreted as a currency amount.

    This function checks if the input is a string that represents a currency amount,
    which could be just a number (with or without decimal points) or a currency code
    followed by a space and a number. It handles both positive and negative amounts.

    Parameters:
    - val: The value to check. Can be of any type.

    Returns:
    - bool: True if `val` appears to represent a currency amount, False otherwise.
    """
    if pd.isna(val):
        return False
    # This regex matches currency patterns like "50", "-40", or "EUR 40.00"
    if re.match(r'^-?\d+(?:\.\d+)?$', val) or re.match(r'^[a-zA-Z]{3} \d+(?:\.\d+)?$', val):
        return True
    return False