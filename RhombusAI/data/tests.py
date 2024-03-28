from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import os

class UploadFileTest(TestCase):
    def test_upload_file_view_with_csv(self):
        # Using reverse to get the URL by name
        url = reverse('data:upload_file')

        # Assuming 'data/example_data/sample_data.csv' is your file path relative to your project root
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sample_csv_path = os.path.join(base_dir, 'data', 'example_data', 'sample_data.csv')

        # Ensure the file path is correct by checking if the file exists
        self.assertTrue(os.path.exists(sample_csv_path), f"File not found: {sample_csv_path}")

        # Reading the content of the sample CSV file
        with open(sample_csv_path, 'rb') as csv_file:
            file_data = csv_file.read()
        
        # Creating a SimpleUploadedFile object to mimic the file upload in the test
        uploaded_file = SimpleUploadedFile(name='test_sample_data.csv', content=file_data, content_type='text/csv')
        
        # Performing a POST request to the upload_file view with the file
        response = self.client.post(url, {'datafile': uploaded_file})
        
        # Asserting that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Add more assertions here based on the expected response content
