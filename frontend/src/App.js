import './App.css';
import React, { useState } from 'react';
import FileUploadComponent from './components/FileUploadComponent';
import DataTableComponent from './components/DataTableComponent';

/**
 * App - The main component of the application.
 *
 * This component serves as the root of the application. It is responsible for rendering the file upload interface
 * and the data table display. It manages the state for the processed data returned from the file upload and passes
 * it down to the DataTableComponent. Additionally, it handles the successful upload of data by updating its state
 * with the new data and handles the override of data types through a callback function.
 *
 * State:
 * - processedData (Array/Object): Holds the data processed from the uploaded file. Initially set to an empty array,
 *   it gets updated upon successful file upload and when data type overrides are performed.
 *
 * Callbacks:
 * - handleUploadSuccess(data): A function that updates the `processedData` state with the data returned from the
 *   FileUploadComponent upon a successful file upload.
 * - handleOverrideSuccess(newProcessedData, newColumnsWithTypes): A function that updates the `processedData` state
 *   to reflect changes made through the DataTypeOverrideComponent. It merges the new processed data and columns with
 *   types information into the existing state.
 *
 * Children:
 * - FileUploadComponent: A child component used for uploading files. It accepts a callback (`onUploadSuccess`) to
 *   handle the successful upload of a file.
 * - DataTableComponent: A child component that displays the processed data in a tabular format. It accepts the
 *   processed data as props and a callback (`onOverrideSuccess`) to handle the successful override of column data types.
 *
 * Usage:
 * Rendered as the root component in the application, typically in the main `index.js` file.
 */
function App() {
  const [processedData, setProcessedData] = useState([]);

  const handleUploadSuccess = async (data) => {
    setProcessedData(data);
  };

  const handleOverrideSuccess = (newProcessedData, newColumnsWithTypes) => {
    // Update the processedData with the new data and types
    setProcessedData(prevData => ({
      ...prevData,
      processed_data: newProcessedData,
      columns_with_types: newColumnsWithTypes,
    }));
  };

  return (
    <div>
      <h1>Upload a File</h1>
      <FileUploadComponent onUploadSuccess={handleUploadSuccess} />
      <DataTableComponent
        processedData={processedData}
        onOverrideSuccess={handleOverrideSuccess} // pass the callback here
      />
    </div>
  );
}

export default App;