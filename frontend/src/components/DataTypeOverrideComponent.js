// import React, { useState } from 'react';

// function DataTypeOverrideComponent({ columnsWithTypes, onSubmitOverride }) {
//   const [selectedColumn, setSelectedColumn] = useState('');
//   const [newDataType, setNewDataType] = useState('');

//   const handleSubmit = (e) => {
//     e.preventDefault();
//     if (!selectedColumn || !newDataType) {
//       alert('Please select a column and enter a new data type.');
//       return;
//     }
//     onSubmitOverride(selectedColumn, newDataType);
//   };

//   return (
//     <div>
//       <h3>Override Column Data Types</h3>
//       <form onSubmit={handleSubmit}>
//         <label>
//           Column:
//           <select value={selectedColumn} onChange={e => setSelectedColumn(e.target.value)}>
//             <option value="">Select Column</option>
//             {columnsWithTypes.map((item, index) => (
//               <option key={index} value={item.column}>{item.column}</option>
//             ))}
//           </select>
//         </label>
//         <label>
//           New Data Type:
//           <input type="text" value={newDataType} onChange={e => setNewDataType(e.target.value)} placeholder="Enter new data type" />
//         </label>
//         <button type="submit">Override</button>
//       </form>
//     </div>
//   );
// }

// export default DataTypeOverrideComponent;
