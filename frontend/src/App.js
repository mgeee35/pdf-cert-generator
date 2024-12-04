import React, { useState } from 'react';
import CertificateForm from './components/CertificateForm';
import CertificateDisplay from './components/CertificateDisplay';

function App() {
  const [certificateData, setCertificateData] = useState(null); // State to store the form data

  // Handle form submission and update certificate data state
  const handleFormSubmit = (data) => {
    setCertificateData(data); // Store the submitted data in state
  };

  return (
    <div className="App">
      <h1>Training Certificate Generator</h1>
      {/* If certificate data is not available, show the form. If data is available, show the certificate display */}
      {!certificateData ? (
        <CertificateForm onSubmit={handleFormSubmit} /> // Show form when data is not available
      ) : (
        <CertificateDisplay data={certificateData} /> // Show certificate display after submission
      )}
    </div>
  );
}

export default App;
