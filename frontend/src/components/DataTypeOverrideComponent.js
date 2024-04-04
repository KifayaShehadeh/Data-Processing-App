import React, { useState } from 'react';

/**
 * DataTypeOverrideComponent - A React component to override the data type of a column.
 *
 * This component allows users to select a column from a provided list and assign a new data type to it. It submits
 * the change to a server endpoint using the Fetch API. Upon successful submission, it can display success or error
 * messages based on the response and invokes a callback function to inform the parent component of the change.
 *
 * Props:
 * - columnsWithTypes (Array): An array of objects where each object represents a column with its current data type.
 *   Each object should have a 'column' key indicating the column name. This prop is required for the component to
 *   function as intended.
 * - onSubmitOverride (function): A callback function that is called when a data type override is successfully
 *   submitted. The function receives the server response data as its argument. This allows the parent component to
 *   react to the submission (e.g., by updating its state or UI).
 *
 * Usage:
 * <DataTypeOverrideComponent
 *   columnsWithTypes={[
 *     { column: 'Column1', type: 'Integer' },
 *     { column: 'Column2', type: 'Text' },
 *     // Add more columns as needed
 *   ]}
 *   onSubmitOverride={(data) => {
 *     console.log('Override successful:', data);
 *   }}
 * />
 *
 * The component renders a form with two dropdowns: one for selecting the column to override and another for selecting
 * the new data type. It supports several predefined data types such as 'Date', 'Integer', 'Boolean', etc. Once the
 * user selects both a column and a new data type and submits the form, the component attempts to post this information
 * to a server endpoint.
 *
 * Upon a successful submission, it displays a success message and calls the `onSubmitOverride` callback function with
 * the response data. If an error occurs during submission, it displays an error message.
 *
 * Note:
 * - The server URL is hardcoded to 'http://127.0.0.1:8000/data/override/'. This may need to be updated to match the
 *   actual URL of your backend server.
 * - The component initialises with no column or data type selected and requires the user to make selections before
 *   submission. It also resets its selections upon a successful submission.
 * - The component does minimal validation and error handling. You may need to extend these functionalities based on
 *   your requirements.
 */
function DataTypeOverrideComponent({ columnsWithTypes, onSubmitOverride }) {
  const [selectedColumn, setSelectedColumn] = useState('');
  const [newDataType, setNewDataType] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Defined valid data types as an array
  const validDataTypes = ['Date', 'Integer', 'Time Duration', 'Boolean', 'Complex Number', 'Category', 'Text', 'Decimal']

 
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');  // Clear any existing errors
    setSuccess(''); // Clear any existing success message
    if (!selectedColumn || !newDataType) {
      setError('Please select a column and enter a new data type.');
      return;
    }
  
    try {
      const response = await fetch('https://data-processing-app-2.onrender.com/data/override/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ column: selectedColumn, new_type: newDataType }),
      });
  
      const data = await response.json();
      if (response.ok) {
        setSuccess(data.message || 'Data type overridden successfully.'); // Set success message
        onSubmitOverride(data);
      } else {
        setError(data.error || 'An error occurred.');
      }
    } catch (error) {
      setError('Error making the request: ' + error.message);
    }
  
    setSelectedColumn('');
    setNewDataType('');
  };

  return (
    <div>
      <h3>Override Column Data Types</h3>
      {success && <div className="success-message">{success}</div>} {/* Add this line */}
      {error && <div className="error-message">{error}</div>} {/* Add this line */}
      <form onSubmit={handleSubmit}>
        <label>
          Column:
          <select value={selectedColumn} onChange={e => setSelectedColumn(e.target.value)}>
            <option value="">Select Column</option>
            {columnsWithTypes.map((item, index) => (
              <option key={index} value={item.column}>{item.column}</option>
            ))}
          </select>
        </label>
        <label>
          New Data Type:
          <select value={newDataType} onChange={e => setNewDataType(e.target.value)}>
            <option value="">Select Data Type</option>
            {validDataTypes.map((type, index) => (
              <option key={index} value={type}>{type}</option>
            ))}
          </select>
        </label>
        <button type="submit">Override</button>
      </form>
    </div>
  );

}

export default DataTypeOverrideComponent;
