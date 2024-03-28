import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Dataset
from .utils import infer_and_convert_data_types, override_data, get_user_friendly_dtype, serialise_dataframe
import pandas as pd
import traceback

@csrf_exempt
def upload_file(request):
    """
    Handles file uploads, supporting CSV and XLSX formats. This view processes the uploaded file to infer and convert
    data types of each column, and returns a JSON response containing processed data and columns with data types.

    Request:
    - Method: POST
    - Body: Multipart form data with a key 'datafile' containing the file to be uploaded.
    - Supported file formats: .csv, .xlsx

    Response:
    - On success: Returns HTTP 200 with JSON { 'processed_data': [...], 'columns_with_types': [...] }
    - On error: Returns HTTP 400 for bad requests (e.g., no file provided or unsupported file format), or HTTP 500 for
      internal errors.

    Side effects:
    - Saves the uploaded file and its processed metadata (including column data types) to the database.
    """
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
            processed_data_list = serialise_dataframe(processed_df)
            columns_with_types = [{'column': col, 'data_type': get_user_friendly_dtype(dtype)} for col, dtype in zip(processed_df.columns, processed_df.dtypes)]

            # Save the uploaded data and column types to the database
            dataset = Dataset(file_name=datafile.name, original_file=datafile)
            dataset.save()
            for col_name, inferred_type in zip(processed_df.columns, processed_df.dtypes):
                user_friendly_type = get_user_friendly_dtype(inferred_type)
                dataset.column_types.create(column_name=col_name, original_type=str(inferred_type), inferred_type=str(inferred_type), user_modified_type=user_friendly_type)
            return JsonResponse({'processed_data': processed_data_list, 'columns_with_types': columns_with_types})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)

@csrf_exempt
def override_data_type(request):
    """
    Allows clients to override the data type of a specific column in the most recently uploaded dataset. It reads
    the dataset from the file system, applies the override, updates the database, and returns the updated dataset
    and column types.

    Request:
    - Method: POST
    - Body: JSON containing 'column' (name of the column to override) and 'new_type' (the new data type to apply).
      Example: { "column": "ColumnName", "new_type": "Integer" }

    Response:
    - On success: Returns HTTP 200 with JSON containing the updated 'processed_data' and 'columns_with_types', along
      with a success message.
    - On error: Returns HTTP 400 for bad requests (e.g., no dataset available, invalid JSON), HTTP 500 for internal
      errors.

    Side effects:
    - Updates the user-defined column data type in the database for the most recent dataset.
    - Does not modify the original file but alters the representation of its data in subsequent responses.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            column = data.get('column')
            new_type = data.get('new_type')

            # Get the most recent dataset
            dataset = Dataset.objects.order_by('-uploaded_at').first()

            if dataset is None:
                return JsonResponse({'error': 'No dataset available to modify.'}, status=400)

            file_path = dataset.original_file.path
            if file_path.lower().endswith('.csv'):
                try:
                    last_uploaded_df = pd.read_csv(file_path)
                except Exception as e:
                    return JsonResponse({'error': f'Error reading CSV file: {str(e)}'}, status=500)
            elif file_path.lower().endswith('.xlsx'):
                try:
                    last_uploaded_df = pd.read_excel(file_path)
                except Exception as e:
                    return JsonResponse({'error': f'Error reading Excel file: {str(e)}'}, status=500)
            else:
                return JsonResponse({'error': 'Unsupported file format. Only .csv and .xlsx are supported.'}, status=400)

            # Retrieve column types from the database
            column_types = dataset.column_types.all()
            column_types_dict = {col.column_name: col for col in column_types}

            success, message = override_data(last_uploaded_df, column, new_type)

            if success:
                # Update column type in the database
                column_obj = column_types_dict[column]
                column_obj.user_modified_type = new_type
                column_obj.save()

                # Update columns_with_types
                columns_with_types = [
                    {'column': col.column_name, 'data_type': col.user_modified_type or col.inferred_type}
                    for col in column_types
                ]

                processed_data_list = serialise_dataframe(last_uploaded_df)

                return JsonResponse({
                    'processed_data': processed_data_list,
                    'columns_with_types': columns_with_types,
                    'message': message  # Include success message
                })
            else:
                return JsonResponse({'error': message}, status=500)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)
