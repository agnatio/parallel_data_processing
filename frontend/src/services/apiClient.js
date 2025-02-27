// src/services/apiClient.js
import axios from 'axios';

// Create axios instance with base URL
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const dataService = {
  // Generate data with parameters
  generateData(params) {
    return apiClient.get('/api/data/generate', { params });
  },
  
  // Get sample data
  getSample(sampleType, params) {
    return apiClient.get(`/api/data/sample/${sampleType}`, { params });
  },
  
  // Upload a file
  uploadFile(formData) {
    return apiClient.post('/api/data/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }
};

export default apiClient;