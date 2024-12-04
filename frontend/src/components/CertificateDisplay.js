import React from 'react';
import { jsPDF } from 'jspdf';

// Component to display certificate details and generate PDF
const CertificateDisplay = ({ data }) => {
  // Function to generate PDF when button is clicked
  const generatePDF = () => {
    const doc = new jsPDF();
    doc.setFontSize(16);
    doc.text(`Certificate Number: ${data.certificateNumber}`, 10, 10); // Add certificate number
    doc.text(`Name: ${data.name} ${data.surname}`, 10, 20); // Add full name
    doc.text(`Training Name: ${data.trainingName}`, 10, 30); // Add training name
    doc.text(`Training Duration: ${data.trainingDuration}`, 10, 40); // Add training duration
    doc.text(`Training Date: ${data.trainingDate}`, 10, 50); // Add training date
    doc.save(`certificate-${data.certificateNumber}.pdf`); // Save the generated PDF with certificate number as filename
  };

  return (
    <div>
      <h2>Certificate Details</h2>
      <p>Certificate Number: {data.certificateNumber}</p>
      <p>Name: {data.name} {data.surname}</p>
      <p>Training Name: {data.trainingName}</p>
      <p>Training Duration: {data.trainingDuration}</p>
      <p>Training Date: {data.trainingDate}</p>
      <button onClick={generatePDF}>Download as PDF</button> {/* Button to generate PDF */}
    </div>
  );
};

export default CertificateDisplay;
