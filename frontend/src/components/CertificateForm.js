import React, { useState } from "react";
import { TextField, Button, Box } from "@mui/material";

// CertificateForm component
// This component renders a form to collect data for a training certificate
const CertificateForm = ({ onSubmit }) => {
  // State to store form data
  const [formData, setFormData] = useState({
    certificateNumber: "", // Certificate number field
    name: "",              // First name field
    surname: "",           // Last name field
    trainingName: "",      // Training name field
    trainingDuration: "",  // Training duration field
    trainingDate: "",      // Training date field
  });

  // Handle changes to form inputs
  const handleChange = (e) => {
    const { name, value } = e.target; // Extract input name and value
    setFormData((prevData) => ({
      ...prevData, // Preserve previous form data
      [name]: value, // Update the value of the specific input
    }));
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault(); // Prevent default form submission
    onSubmit(formData); // Pass form data to the parent component
  };

  // Render the form
  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        maxWidth: "400px", // Limit the width of the form
        margin: "0 auto", // Center the form
        padding: "20px", // Add padding around the form
        backgroundColor: "#fff", // Set the background color to white
        borderRadius: "8px", // Add rounded corners
        boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.1)", // Add a shadow effect
      }}
    >
      <h2 style={{ textAlign: "center", marginBottom: "20px" }}>
        Training Certificate Form
      </h2>

      {/* Input field for certificate number */}
      <TextField
        label="Certificate Number"
        name="certificateNumber"
        value={formData.certificateNumber}
        onChange={handleChange}
        fullWidth
        required
        margin="normal"
      />

      {/* Input field for first name */}
      <TextField
        label="First Name"
        name="name"
        value={formData.name}
        onChange={handleChange}
        fullWidth
        required
        margin="normal"
      />

      {/* Input field for last name */}
      <TextField
        label="Last Name"
        name="surname"
        value={formData.surname}
        onChange={handleChange}
        fullWidth
        required
        margin="normal"
      />

      {/* Input field for training name */}
      <TextField
        label="Training Name"
        name="trainingName"
        value={formData.trainingName}
        onChange={handleChange}
        fullWidth
        required
        margin="normal"
      />

      {/* Input field for training duration */}
      <TextField
        label="Training Duration"
        name="trainingDuration"
        value={formData.trainingDuration}
        onChange={handleChange}
        fullWidth
        required
        margin="normal"
      />

      {/* Input field for training date */}
      <TextField
        label="Training Date"
        name="trainingDate"
        type="date" // Use date input type
        InputLabelProps={{ shrink: true }} // Ensure the label stays above the input
        value={formData.trainingDate}
        onChange={handleChange}
        fullWidth
        required
        margin="normal"
      />

      {/* Submit button */}
      <Button
        type="submit"
        variant="contained"
        color="primary"
        fullWidth
        sx={{ marginTop: "16px" }}
      >
        Create Certificate
      </Button>
    </Box>
  );
};

export default CertificateForm;
