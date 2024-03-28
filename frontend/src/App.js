import './App.css';

import React, { useState } from 'react';
import FileUploadComponent from './components/FileUploadComponent';
import DataTableComponent from './components/DataTableComponent';

function App() {
  const [processedData, setProcessedData] = useState([]);

  const handleUploadSuccess = async (data) => {
   
    console.log("plsss", data)
    console.log(data.processed_data[0])
    setProcessedData(data);
    console.log("again", processedData)
  };

  return (
    <div>
      <h1>Upload a File</h1>
      <FileUploadComponent onUploadSuccess={handleUploadSuccess} />
      <DataTableComponent processedData={processedData} />
    </div>
  );
}

export default App;