<template>
    <div class="data-generator">
        <h1>Data Generator</h1>

        <div class="generator-container">
            <div class="controls-panel">
                <div class="form-group">
                    <label for="rows">Rows:</label>
                    <input id="rows" v-model.number="rows"
                           type="number" min="1" max="1000"
                           class="form-control" />
                </div>

                <div class="form-group">
                    <label for="columns">Columns:</label>
                    <input id="columns"
                           v-model.number="columns"
                           type="number" min="1" max="20"
                           class="form-control" />
                </div>

                <div class="form-group">
                    <label for="format">Output
                        Format:</label>
                    <select id="format"
                            v-model="selectedFormat"
                            class="form-control">
                        <option value="json">JSON</option>
                        <option value="csv">CSV</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="toggle-label">
                        <input type="checkbox"
                               v-model="showAdvancedOptions" />
                        Show Advanced Options
                    </label>
                </div>

                <div v-if="showAdvancedOptions"
                     class="advanced-options">
                    <h3>Data Types</h3>
                    <p class="help-text">Specify data types
                        for each column</p>

                    <div class="data-types-list">
                        <div v-for="(type, index) in selectedDataTypes"
                             :key="index"
                             class="data-type-item">
                            <select v-model="selectedDataTypes[index]"
                                    class="form-control data-type-select">
                                <option v-for="type in availableDataTypes"
                                        :key="type"
                                        :value="type">
                                    {{ type }}
                                </option>
                            </select>
                            <button @click="removeDataType(index)"
                                    class="btn btn-danger btn-sm">✕</button>
                        </div>
                    </div>

                    <button @click="addDataType"
                            class="btn btn-primary btn-sm add-type-btn"
                            v-if="selectedDataTypes.length < columns">
                        Add Data Type
                    </button>
                </div>

                <div class="action-buttons">
                    <button @click="generateData"
                            class="btn btn-primary"
                            :disabled="loading">
                        {{ loading ? 'Generating...' :
                        'Generate Data' }}
                    </button>

                    <button @click="downloadData"
                            class="btn btn-success"
                            :disabled="loading || !hasGeneratedData">
                        Download {{
                        selectedFormat.toUpperCase() }}
                    </button>

                    <div class="dropdown">
                        <button class="btn btn-info dropdown-toggle"
                                @click="toggleSampleDropdown">
                            Sample Data
                        </button>
                        <div class="dropdown-menu"
                             v-if="showSampleDropdown">
                            <a v-for="sample in sampleTypes"
                               :key="sample"
                               @click="downloadSample(sample)"
                               class="dropdown-item">
                                {{ sample }}
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            <div class="preview-panel">
                <div v-if="error" class="error-message">
                    {{ error }}
                </div>

                <div v-if="loading"
                     class="loading-container">
                    <div class="spinner"></div>
                    <p>Generating data...</p>
                </div>

                <!-- Display for JSON data -->
                <div v-if="jsonData && selectedFormat === 'json'"
                     class="data-preview json-preview">
                    <h2>JSON Preview</h2>
                    <div class="metadata-info">
                        <span><strong>Rows:</strong> {{
                            jsonData.metadata.rows }}</span>
                        <span><strong>Columns:</strong> {{
                            jsonData.metadata.columns
                            }}</span>
                    </div>

                    <div class="table-responsive">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th v-for="(header, index) in jsonData.metadata.headers"
                                        :key="index">
                                        {{ header }}
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(row, rowIndex) in jsonPreviewData"
                                    :key="rowIndex">
                                    <td v-for="(column, columnIndex) in jsonData.metadata.headers"
                                        :key="columnIndex">
                                        {{ row[column] }}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="raw-data-toggle">
                        <button @click="toggleRawJson"
                                class="btn btn-sm btn-secondary">
                            {{ showRawJson ? 'Hide' : 'Show'
                            }} Raw JSON
                        </button>

                        <pre v-if="showRawJson"
                             class="raw-data">{{ JSON.stringify(jsonData, null, 2) }}</pre>
                    </div>
                </div>

                <!-- Display for CSV data -->
                <div v-if="csvData && selectedFormat === 'csv'"
                     class="data-preview csv-preview">
                    <h2>CSV Preview</h2>

                    <div class="table-responsive">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th v-for="(header, index) in csvHeaders"
                                        :key="index">
                                        {{ header }}
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(row, rowIndex) in csvRows"
                                    :key="rowIndex">
                                    <td v-for="(cell, cellIndex) in row"
                                        :key="cellIndex">
                                        {{ cell }}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="raw-data-toggle">
                        <button @click="toggleRawCsv"
                                class="btn btn-sm btn-secondary">
                            {{ showRawCsv ? 'Hide' : 'Show'
                            }} Raw CSV
                        </button>

                        <pre v-if="showRawCsv"
                             class="raw-data">{{ csvData }}</pre>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'DataGenerator',
    data() {
        return {
            // Form inputs
            rows: 10,
            columns: 10,
            selectedFormat: 'json',
            showAdvancedOptions: false,
            selectedDataTypes: [],

            // Data state
            jsonData: null,
            csvData: null,
            loading: false,
            error: '',
            showSampleDropdown: false,
            showRawJson: false,
            showRawCsv: false,

            // Available options
            availableDataTypes: [
                'string', 'integer', 'float', 'date', 'boolean',
                'email', 'name', 'address', 'product', 'price'
            ],

            sampleTypes: ['users', 'products', 'transactions']
        };
    },

    computed: {
        hasGeneratedData() {
            return (this.selectedFormat === 'json' && this.jsonData) ||
                (this.selectedFormat === 'csv' && this.csvData);
        },

        jsonPreviewData() {
            if (this.jsonData && this.jsonData.data) {
                // Return up to 5 rows for preview
                return this.jsonData.data.slice(0, 5);
            }
            return [];
        },

        csvHeaders() {
            if (this.csvData) {
                const lines = this.csvData.split('\n');
                if (lines.length > 0) {
                    return this.parseCsvLine(lines[0]);
                }
            }
            return [];
        },

        csvRows() {
            if (this.csvData) {
                const lines = this.csvData.split('\n');
                if (lines.length > 1) {
                    // Return up to 5 rows for preview
                    return lines.slice(1, 6)
                        .filter(line => line.trim().length > 0)
                        .map(line => this.parseCsvLine(line));
                }
            }
            return [];
        }
    },

    watch: {
        columns(newValue) {
            // Reset data types if columns change
            if (this.selectedDataTypes.length > newValue) {
                this.selectedDataTypes = this.selectedDataTypes.slice(0, newValue);
            }
        },

        selectedFormat() {
            // Clear data when format changes
            if (this.selectedFormat === 'json') {
                this.csvData = null;
            } else {
                this.jsonData = null;
            }
        }
    },

    methods: {
        addDataType() {
            if (this.selectedDataTypes.length < this.columns) {
                this.selectedDataTypes.push(this.availableDataTypes[0]);
            }
        },

        removeDataType(index) {
            this.selectedDataTypes.splice(index, 1);
        },

        toggleSampleDropdown() {
            this.showSampleDropdown = !this.showSampleDropdown;
        },

        toggleRawJson() {
            this.showRawJson = !this.showRawJson;
        },

        toggleRawCsv() {
            this.showRawCsv = !this.showRawCsv;
        },

        parseCsvLine(line) {
            // Basic CSV parsing (not handling quoted values properly for brevity)
            return line.split(',').map(field => field.trim());
        },

        async generateData() {
            this.loading = true;
            this.error = '';

            try {
                // Prepare query parameters
                const params = new URLSearchParams();
                params.append('rows', this.rows);
                params.append('columns', this.columns);
                params.append('format', this.selectedFormat);

                // Add data types if specified
                if (this.showAdvancedOptions && this.selectedDataTypes.length > 0) {
                    this.selectedDataTypes.forEach(type => {
                        params.append('data_types', type);
                    });
                }

                // Use API URL from environment variable or default
                const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

                // Fetch data from API
                const response = await fetch(`${apiUrl}/api/data/generate?${params.toString()}`);

                if (!response.ok) {
                    throw new Error(`Failed to generate data: ${response.statusText}`);
                }

                // Process based on selected format
                if (this.selectedFormat === 'json') {
                    this.jsonData = await response.json();
                    this.csvData = null;
                } else {
                    this.csvData = await response.text();
                    this.jsonData = null;
                }
            } catch (err) {
                console.error('Error generating data:', err);
                this.error = err.message || 'Failed to generate data';
            } finally {
                this.loading = false;
            }
        },

        async downloadData() {
            if (!this.hasGeneratedData) return;

            try {
                // Prepare query parameters
                const params = new URLSearchParams();
                params.append('rows', this.rows);
                params.append('columns', this.columns);
                params.append('format', this.selectedFormat);

                // Add data types if specified
                if (this.showAdvancedOptions && this.selectedDataTypes.length > 0) {
                    this.selectedDataTypes.forEach(type => {
                        params.append('data_types', type);
                    });
                }

                // Use API URL from environment variable or default
                const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

                // Create a direct download link
                const downloadUrl = `${apiUrl}/api/data/generate?${params.toString()}`;

                // Create an anchor element and trigger download
                const a = document.createElement('a');
                a.href = downloadUrl;
                a.download = `generated_data_${this.rows}x${this.columns}.${this.selectedFormat}`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            } catch (err) {
                console.error('Error downloading data:', err);
                this.error = err.message || 'Failed to download data';
            }
        },

        async downloadSample(sampleType) {
            try {
                this.showSampleDropdown = false;

                // Use API URL from environment variable or default
                const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

                // Create a direct download link with the selected sample type
                const downloadUrl = `${apiUrl}/api/data/sample/${sampleType}?rows=${this.rows}&format=${this.selectedFormat}`;

                // Create an anchor element and trigger download
                const a = document.createElement('a');
                a.href = downloadUrl;
                a.download = `${sampleType}_sample.${this.selectedFormat}`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            } catch (err) {
                console.error('Error downloading sample:', err);
                this.error = err.message || 'Failed to download sample';
            }
        }
    }
};
</script>

<style scoped>
.data-generator {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
}

.generator-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.controls-panel {
    flex: 1;
    min-width: 300px;
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.preview-panel {
    flex: 2;
    min-width: 500px;
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
    margin-bottom: 15px;
}

.form-control {
    display: block;
    width: 100%;
    padding: 8px 12px;
    font-size: 16px;
    border: 1px solid #ced4da;
    border-radius: 4px;
}

.toggle-label {
    display: flex;
    align-items: center;
    cursor: pointer;
}

.toggle-label input {
    margin-right: 8px;
}

.advanced-options {
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid #dee2e6;
}

.help-text {
    font-size: 14px;
    color: #6c757d;
    margin-bottom: 10px;
}

.data-types-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 15px;
}

.data-type-item {
    display: flex;
    gap: 8px;
}

.data-type-select {
    flex: 1;
}

.action-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 25px;
}

.btn {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
}

.btn-primary {
    background-color: #007bff;
    color: white;
}

.btn-success {
    background-color: #28a745;
    color: white;
}

.btn-info {
    background-color: #17a2b8;
    color: white;
}

.btn-secondary {
    background-color: #6c757d;
    color: white;
}

.btn-danger {
    background-color: #dc3545;
    color: white;
}

.btn-sm {
    padding: 4px 8px;
    font-size: 14px;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.dropdown {
    position: relative;
}

.dropdown-menu {
    position: absolute;
    top: 100%;
    left: 0;
    z-index: 1000;
    display: block;
    min-width: 160px;
    padding: 8px 0;
    margin-top: 4px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.dropdown-item {
    display: block;
    padding: 8px 16px;
    cursor: pointer;
}

.dropdown-item:hover {
    background-color: #f8f9fa;
}

.error-message {
    padding: 12px;
    background-color: #f8d7da;
    color: #721c24;
    border-radius: 4px;
    margin-bottom: 20px;
}

.loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 0;
}

.spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    border-top: 4px solid #007bff;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin-bottom: 16px;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.data-preview {
    padding: 15px;
    border: 1px solid #dee2e6;
    border-radius: 4px;
}

.metadata-info {
    display: flex;
    gap: 20px;
    margin-bottom: 15px;
    font-size: 14px;
}

.table-responsive {
    overflow-x: auto;
    margin-bottom: 20px;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table th,
.data-table td {
    padding: 8px;
    border: 1px solid #dee2e6;
    text-align: left;
}

.data-table th {
    background-color: #f8f9fa;
    font-weight: 600;
}

.data-table tr:nth-child(even) {
    background-color: #f2f2f2;
}

.raw-data-toggle {
    margin-top: 15px;
}

.raw-data {
    max-height: 400px;
    overflow: auto;
    padding: 15px;
    margin-top: 10px;
    background-color: #f8f9fa;
    border-radius: 4px;
    font-family: monospace;
    font-size: 14px;
    white-space: pre-wrap;
}

@media (max-width: 768px) {
    .generator-container {
        flex-direction: column;
    }
}
</style>