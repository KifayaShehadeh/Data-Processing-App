from django.db import models

class Dataset(models.Model):
    """
    Represents an uploaded dataset file within the application.

    Fields:
    - uploaded_at (DateTimeField): The date and time when the dataset was uploaded. Automatically set to the current date/time when a dataset is created.
    - file_name (CharField): The name of the uploaded file.
    - processed_at (DateTimeField): The date and time when the dataset was processed. Optional and can be blank.
    - original_file (FileField): A file field that stores the uploaded dataset file. Files are uploaded to the 'datasets/' directory.
    - processed_data (TextField): Field to store the processed data as a JSON string.

    Methods:
    - __str__(self): Returns a human-readable string representation of the model, which is the file name of the uploaded dataset.
    """
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    processed_at = models.DateTimeField(null=True, blank=True)
    original_file = models.FileField(upload_to='datasets/')
    processed_data = models.TextField(blank=True, null=True)  # New field to store processed data
    processed_file_pkl = models.BinaryField(null=True, blank=True)

    def str(self):
        return self.file_name

class ColumnType(models.Model):
    """
    Stores information about the data types of columns within a dataset.

    Fields:
    - dataset (ForeignKey): A ForeignKey link to the 'Dataset' model that this column type information belongs to. 
      This establishes a many-to-one relationship where a dataset can have many column types.
    - column_name (CharField): The name of the column.
    - original_type (CharField): The original data type of the column as detected by the system.
    - inferred_type (CharField): The data type of the column after being inferred/processed by the system.
    - user_modified_type (CharField): The data type of the column after a user has optionally modified it. This field can be blank.

    Methods:
    - __str__(self): Returns a string representation of the model, including the column name, dataset file name, original, and inferred data types.
    """
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='column_types')
    column_name = models.CharField(max_length=255)
    original_type = models.CharField(max_length=50)
    inferred_type = models.CharField(max_length=50)
    user_modified_type = models.CharField(max_length=50, blank=True, null=True)

    def str(self):
        return f"{self.column_name} in {self.dataset.file_name} - Original: {self.original_type}, Inferred: {self.inferred_type}"