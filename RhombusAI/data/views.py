import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import infer_and_convert_data_types
import pandas as pd
import traceback


def get_user_friendly_dtype(dtype):
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
    
def serialize_dataframe(df):
    """Convert a DataFrame to a list of dicts with JSON serializable values, converting NaN to None (null in JSON)."""
    df = df.copy()
    for column in df.columns:
        dtype = df[column].dtype
        if pd.api.types.is_datetime64_any_dtype(dtype):
            df[column] = df[column].dt.strftime('%Y-%m-%d %H:%M:%S').replace(pd.NaT, None)
        elif pd.api.types.is_timedelta64_dtype(dtype):
            df[column] = df[column].apply(lambda x: x.total_seconds() if pd.notnull(x) else None)
        elif pd.api.types.is_categorical_dtype(dtype) or pd.api.types.is_object_dtype(dtype):
            df[column] = df[column].astype(str).replace({'nan': None, 'None': None})
        elif pd.api.types.is_complex_dtype(dtype):
            df[column] = df[column].apply(lambda x: str(x) if pd.notnull(x) else None)

        else:
            print(df[column] )
            # Convert NaN values to None, which will be serialized as null in JSON
            df[column] = df[column].apply(lambda x: 'N/A' if pd.isnull(x) else x)
    
    return df.to_dict(orient='records')

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        datafile = request.FILES.get('datafile', None)
        if datafile is None:
            return JsonResponse({'error': 'No file provided.'}, status=400)

        try:
            if str(datafile.name).lower().endswith('.csv'):
                df = pd.read_csv(datafile)
            elif str(datafile.name).lower().endswith('.xlsx'):
                df = pd.read_excel(datafile)
            else:
                return JsonResponse({'error': 'Unsupported file format. Only .csv and .xlsx are supported.'}, status=400)

            processed_df = infer_and_convert_data_types(df)
            processed_data_list = serialize_dataframe(processed_df)
            print(json.dumps(processed_data_list, indent=4))
            columns_with_types = [{'column': col, 'data_type': get_user_friendly_dtype(dtype)} for col, dtype in zip(processed_df.columns, processed_df.dtypes)]

            print(json.dumps(columns_with_types, indent=4))
            return JsonResponse({'processed_data': processed_data_list, 'columns_with_types': columns_with_types})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)
    
