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

def convert_to_datetime(df, col, date_formats):
    converted_col = None
    for date_format in date_formats:
        try:
            converted_col = pd.to_datetime(df[col], errors='coerce', format=date_format)
            if converted_col.notna().any():
                break
        except ValueError:
            continue
    return converted_col if converted_col is not None and converted_col.notna().any() else df[col]

def convert_to_numeric(df, col):
    converted_col = pd.to_numeric(df[col], errors='coerce')
    if converted_col.notna().any():
        df[col] = converted_col
        if df[col].dtype == 'float':
            df[col] = pd.to_numeric(df[col], downcast='float')
        elif df[col].dtype == 'int':
            df[col] = pd.to_numeric(df[col], downcast='integer')
    return df[col]

def convert_to_timedelta(df, col):
    converted_col = pd.to_timedelta(df[col], errors='coerce')
    return converted_col if converted_col.notna().any() else df[col]

def convert_to_boolean(df, col):
    if all(val.lower() in ['true', 'false'] for val in df[col].astype(str).str.lower()):
        return df[col].astype(bool)
    return df[col]

def convert_to_complex(df, col, is_complex):
    if is_complex(df[col]):
        return df[col].apply(lambda x: complex(x) if pd.notna(x) else x)
    return df[col]

def convert_to_categorical(df, col, is_category):
    if is_category(df[col]):
        return df[col].astype('category')
    return df[col]

def infer_and_convert_data_types(df):
    date_formats = [
        '%Y-%m-%d',  # Standard YYYY-MM-DD
        '%d-%m-%Y',  # Non-standard DD-MM-YYYY
        '%m/%d/%Y',  # Standard MM/DD/YYYY
        '%d/%m/%Y',  # Standard DD/MM/YYYY
        '%Y/%m/%d',  # Non-standard YYYY/MM/DD
        '%Y%m%d',    # Standard YYYYMMDD
        '%m/%Y',      # Standard MM/YYYY
        '%Y/%m',      # Non-standard YYYY/MM
        '%m.%d.%Y',  # Non-standard MM.DD.YYYY
        '%d.%m.%Y',  # Non-standard DD.MM.YYYY
        '%d %B',     # Non-standard DD Month (e.g., 01 January)
        '%d%B',      # Non-standard DDMonth (e.g., 01January)
        '%B %d',     # Non-standard Month DD (e.g., January 01)
        '%B%d',      # Non-standard MonthDD (e.g., January01)
        '%d %B %Y',  # Non-standard DD Month YYYY (e.g., 01 January 2022)
        '%d%B%Y',    # Non-standard DDMonthYYYY (e.g., 01January2022)
        '%B %d, %Y', # Non-standard Month DD, YYYY (e.g., January 01, 2022) **
        '%Y %B %d',   # Non-standard YYYY Month DD (e.g., 2022 January 01)
        '%B %Y',       # Non-standard Month Year (e.g., January 2022)
        '%Y %B',       # Non-standard Year Month (e.g., 2022 January)
        '%B%Y',        # Non-standard MonthYear (e.g., January2022)
        '%Y%B',        # Non-standard YearMonth (e.g., 2022January)
    ]

    for col in df.columns:

        if df[col].dtype == object or df[col].dtype == int:
            df[col] = convert_to_datetime(df, col, date_formats)

        if df[col].dtype == object:
            df[col] = convert_to_numeric(df, col)

        if df[col].dtype == object:
            df[col] = convert_to_timedelta(df, col)

        if df[col].dtype == object:
            df[col] = convert_to_boolean(df, col)

        if df[col].dtype == object:
            df[col] = convert_to_complex(df, col, is_complex)

        if df[col].dtype == object:
            df[col] = convert_to_categorical(df, col, is_category)

    return df