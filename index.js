const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

const app = express();
const port = 3000; // Local server on port 3000

// Enable CORS and JSON parsing
app.use(cors());
app.use(express.json());

// Sample metrics and prediction data
const metrics = {
  qualityMetric: 'High',
  predictions: [50, 30, 20], // Percentages for Normal, Inconclusive, and Abnormal test results
};

// Function to load CSV data
const loadHealthcareDataFromCSV = async (filePath) => {
  return new Promise((resolve, reject) => {
    const data = [];
    if (!fs.existsSync(filePath)) {
      return reject(new Error('CSV file not found'));
    }

    fs.createReadStream(filePath)
      .pipe(csv())
      .on('data', (row) => data.push(row))
      .on('end', () => resolve(data))
      .on('error', (err) => reject(err));
  });
};

// Define the /api/metrics endpoint
app.get('/api/metrics', async (req, res) => {
  try {
    const filePath = path.join(__dirname, 'cleaned_healthcare_dataset.csv');
    const healthcareData = await loadHealthcareDataFromCSV(filePath);

    res.json({ ...metrics, data: healthcareData });
  } catch (error) {
    console.error('Error loading CSV:', error.message);
    res.status(500).json({ error: error.message });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`✅ Server running at http://localhost:${port}/`);
});