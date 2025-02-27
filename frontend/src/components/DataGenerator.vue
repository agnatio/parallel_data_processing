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
