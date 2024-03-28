import React, { useState } from 'react';
import DataTypeOverrideComponent from './DataTypeOverrideComponent';

/**
 * DataTableComponent - A React component for displaying processed data in a paginated table.
 *
 * This component displays processed data in a tabular format, with pagination controls to navigate through the data.
 * It also integrates the DataTypeOverrideComponent to allow overriding the data type of a column directly from the
 * table's interface. The component expects processed data to be passed in as a prop, including both the data rows
 * and metadata about the columns (such as names and data types).
 *
 * Props:
 * - processedData (Object): An object containing processed data and metadata. It should have two keys:
 *   `processed_data`, an array of objects where each object represents a row of data, and `columns_with_types`,
 *   an array of objects detailing columns and their data types.
 * - onOverrideSuccess (function): A callback function that is called when the data type of a column is successfully
 *   overridden. It receives the updated processed data and columns metadata as its arguments.
 *
 * Usage:
 * <DataTableComponent
 *   processedData={{
 *     processed_data: [{ Column1: 'Value1', Column2: 'Value2' }, ...],
 *     columns_with_types: [{ column: 'Column1', data_type: 'Text' }, ...]
 *   }}
 *   onOverrideSuccess={(processedData, columnsWithTypes) => {
 *     // Handle the successful override (e.g., update state or UI)
 *   }}
 * />
 *
 * The component first checks if the `processedData` prop is provided and contains data; if not, it renders nothing.
 * It calculates the total number of pages based on the data size and the specified `pageSize`. It displays the data
 * for the current page, with column headers showing both the column names and their data types. Below the table,
 * pagination controls ('Previous' and 'Next' buttons) allow the user to navigate through the pages.
 *
 * The DataTypeOverrideComponent is included below the table, allowing users to override the data type of any column.
 * It passes the `columns_with_types` from `processedData` to DataTypeOverrideComponent and handles the override
 * success by calling the `onOverrideSuccess` prop with the response.
 *
 * Note:
 * - This component is designed to work with data structures specific to its props. Ensure your data conforms to the
 *   expected format.
 * - The `pageSize` is currently set to 5 rows per page and can be adjusted as needed.
 * - The component uses simple inline styling for the table and pagination controls. Consider using CSS or styled
 *   components for more sophisticated styling and responsiveness.
 */
function DataTableComponent({ processedData, onOverrideSuccess }) {
  const pageSize = 5; // Number of rows per page
  const [currentPage, setCurrentPage] = useState(1);

  if (!processedData || processedData.length === 0) return null;

  const totalPages = Math.ceil(processedData.processed_data.length / pageSize);
  const startIndex = (currentPage - 1) * pageSize;
  const endIndex = startIndex + pageSize;
  const currentData = processedData.processed_data.slice(startIndex, endIndex);

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handleOverride = (response) => {
    onOverrideSuccess(response.processed_data, response.columns_with_types);
  };

  return (
    <div>
      <h2>Processed Data Results</h2>
      <table>
        <thead>
          <tr>
            {processedData.columns_with_types.map((item, index) => (
              <th key={index}>{item.column}</th>
            ))}
          </tr>
          <tr>
            {processedData.columns_with_types.map((item, index) => (
              <th key={index} style={{ textAlign: 'center', background: '#f0f0f0' }}>
                {item.data_type}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {currentData.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {processedData.columns_with_types.map((item, colIndex) => (
                <td key={colIndex}>
                  {typeof row[item.column] === 'boolean' ? row[item.column].toString() : row[item.column]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <div style={{ marginTop: '10px' }}>
        <button onClick={handlePrevPage} disabled={currentPage === 1}>Previous</button>
        <span style={{ margin: '0 10px' }}>Page {currentPage} of {totalPages}</span>
        <button onClick={handleNextPage} disabled={currentPage === totalPages}>Next</button>
      </div>
      <DataTypeOverrideComponent columnsWithTypes={processedData.columns_with_types} onSubmitOverride={handleOverride} />
    </div>
  );
}

export default DataTableComponent;