import React from "react";
import { Button, Card, CardContent, Typography } from "@mui/material";
import { jsPDF } from "jspdf";

// CertificateDisplay component
// This component displays the details of a certificate and allows the user to download it as a PDF
const CertificateDisplay = ({ data }) => {
  // Function to generate a PDF using jsPDF
  const generatePDF = () => {
    const doc = new jsPDF(); // Create a new jsPDF instance
    doc.setFontSize(16); // Set the font size for the text

    // Add certificate details to the PDF
    doc.text(`Certificate Number: ${data.certificateNumber}`, 10, 10);
    doc.text(`Name: ${data.name} ${data.surname}`, 10, 20);
    doc.text(`Training Name: ${data.trainingName}`, 10, 30);
    doc.text(`Training Duration: ${data.trainingDuration}`, 10, 40);
    doc.text(`Training Date: ${data.trainingDate}`, 10, 50);

    // Save the generated PDF file with a dynamic file name
    doc.save(`certificate-${data.certificateNumber}.pdf`);
  };

  // Render the certificate details in a card
  return (
    <Card
      sx={{
        maxWidth: "500px", // Set the maximum width of the card
        margin: "20px auto", // Center the card with margin
        padding: "20px", // Add padding inside the card
        backgroundColor: "#f9f9f9", // Set the background color
        borderRadius: "8px", // Add rounded corners
        boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.1)", // Add a shadow effect
      }}
    >
      <CardContent>
        {/* Display certificate title */}
        <Typography variant="h5" gutterBottom>
          Certificate Details
        </Typography>

        {/* Display certificate fields */}
        <Typography>Certificate Number: {data.certificateNumber}</Typography>
        <Typography>
          Name: {data.name} {data.surname}
        </Typography>
        <Typography>Training Name: {data.trainingName}</Typography>
        <Typography>Training Duration: {data.trainingDuration}</Typography>
        <Typography>Training Date: {data.trainingDate}</Typography>
      </CardContent>

      {/* Button to generate and download the certificate as a PDF */}
      <Button
        variant="contained"
        color="primary"
        fullWidth
        onClick={generatePDF} // Trigger the PDF generation function
        sx={{ marginTop: "16px" }}
      >
        Download as PDF
      </Button>
    </Card>
  );
};

export default CertificateDisplay;
