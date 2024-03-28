import React from 'react';

function DataTableComponent({ processedData }) {
  if (!processedData || processedData.length === 0) return null;

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
          {processedData.processed_data.map((row, rowIndex) => (
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
    </div>
  );
}

export default DataTableComponent;
