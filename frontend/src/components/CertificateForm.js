import React, { useState } from 'react';

// Form component to collect certificate information
const CertificateForm = ({ onSubmit }) => {
  // State to hold form data
  const [formData, setFormData] = useState({
    certificateNumber: '',
    name: '',
    surname: '',
    trainingName: '',
    trainingDuration: '',
    trainingDate: '',
  });

  // Handle input change and update state
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value, // Dynamically update the state based on the input field
    }));
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault(); // Prevent page reload
    onSubmit(formData);  // Pass form data to the parent component
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Certificate Number</label>
        <input
          type="text"
          name="certificateNumber"
          value={formData.certificateNumber}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label>First Name</label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label>Last Name</label>
        <input
          type="text"
          name="surname"
          value={formData.surname}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label>Training Name</label>
        <input
          type="text"
          name="trainingName"
          value={formData.trainingName}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label>Training Duration</label>
        <input
          type="text"
          name="trainingDuration"
          value={formData.trainingDuration}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label>Training Date</label>
        <input
          type="date"
          name="trainingDate"
          value={formData.trainingDate}
          onChange={handleChange}
          required
        />
      </div>
      <button type="submit">Create Certificate</button>
    </form>
  );
};

export default CertificateForm;
