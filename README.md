# RhombusAI

# Data Processing Web Application

This web application is designed to process and display data, focusing on data type inference and conversion for datasets using Python, Pandas, and a React frontend. The application allows users to upload CSV or Excel files, automatically infers data types for each column, and allows for manual data type override.

## Features

- **Pandas Data Type Inference and Conversion:** Utilizes Pandas to infer and convert data types in uploaded datasets.
- **Django Backend:** Incorporates a Django backend to handle data processing logic and user interactions.
- **React Frontend:** A React-based frontend that provides a user-friendly interface for uploading data, viewing processed data, and manually overriding data types.

## Getting Started

### Prerequisites

- Python 3.x
- Django
- Pandas
- Node.js and npm

### Setting Up the Backend

1. Navigate to the backend directory.
2. Install the required Python packages:

`pip install -r requirements.txt`

3. Run the Django migrations to set up your database:

`python manage.py migrate`

4. Start the Django development server:

`python manage.py runserver`


### Setting Up the Frontend

1. Navigate to the frontend directory where `package.json` is located.
2. Install the required Node.js packages:

`npm install`

3. Start the React development server:

`npm start`

This will open the web application in your default browser. If it doesn't automatically open, you can access it by visiting [http://localhost:3000](http://localhost:3000) in your browser.

### Using the Application

1. **Upload a File:** Click on the "Upload" button and select a CSV or Excel file to process. The application will automatically process the file and display the inferred data types.
2. **View Processed Data:** After uploading, the processed data along with the inferred data types will be displayed.
3. **Override Data Types:** *(Feature currently under development)* Users will be able to override the inferred data types by selecting a column and specifying a new data type.

## Additional Notes

This project aims to provide a comprehensive solution for automating data cleaning tasks, with a focus on flexibility and user input. Given the variety of datasets, the application is designed to handle general cases with an understanding that some level of customisation may be necessary.

For detailed information on the data type inference and conversion process, please refer to the provided Python scripts in the backend directory.

