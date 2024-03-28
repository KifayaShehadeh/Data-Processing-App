import React, { useState } from 'react';
import axios from 'axios';

/**
 * FileUploadComponent - A React component for uploading files to a server.
 *
 * This component provides a simple UI for selecting and uploading files. It uses axios for making HTTP POST requests
 * to upload the selected file to a specified server endpoint. The component accepts a single prop, `onUploadSuccess`,
 * which is a callback function that gets called with the response data from the server upon successful upload.
 *
 * Props:
 * - onUploadSuccess (function): A callback function that is called when the file upload is successful. It receives
 *   the response data from the server as its only argument. This prop is optional; if not provided, the component
 *   will log a message to the console instead.
 *
 * Usage:
 * <FileUploadComponent
 *   onUploadSuccess={(data) => {
 *     console.log('Upload successful:', data);
 *   }}
 * />
 *
 * The component displays a file input for the user to select a file. Once a file is selected, an 'Upload' button
 * appears. Clicking this button will start the upload process. The component only accepts `.csv` and `.xlsx` files
 * for upload, but this can be customised via the `accept` attribute of the file input element.
 *
 * Dependencies:
 * - axios: The component uses axios for making HTTP requests. Ensure axios is installed and imported in your project.
 *
 * Note:
 * - The server URL is hardcoded to 'http://127.0.0.1:8000/data/upload/'. You may need to modify this to match your
 *   backend server's URL.
 * - The component handles basic upload functionality and error logging. You may want to extend it with additional
 *   features such as progress indicators, more sophisticated error handling, or support for multiple file uploads.
 */
function FileUploadComponent({ onUploadSuccess }) {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleUploadClick = async (e) => {
    e.preventDefault();
    if (!file) {
      console.error('No file selected');
      return;
    }
    const formData = new FormData();
    formData.append('datafile', file);

    try {
      const response = await axios.post('http://127.0.0.1:8000/data/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      if (typeof onUploadSuccess === 'function') {
        onUploadSuccess(response.data);
      } else {
        console.error('onUploadSuccess is not a function');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <form>
      <input type="file" name="datafile" accept=".csv, .xlsx" onChange={handleFileChange} />
      <button type="button" onClick={handleUploadClick}>Upload</button>
    </form>
  );
}

export default FileUploadComponent;
