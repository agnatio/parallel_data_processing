<template>
    <div class="file-uploader">
        <h1>File Uploader</h1>

        <div class="upload-container">
            <div class="upload-area"
                 @dragover.prevent="handleDragOver"
                 @dragleave.prevent="handleDragLeave"
                 @drop.prevent="handleDrop"
                 :class="{ 'drag-over': isDragOver }">
                <div class="upload-content">
                    <div class="upload-icon">
                        <svg xmlns="http://www.w3.org/2000/svg"
                             viewBox="0 0 24 24" width="48"
                             height="48" fill="none"
                             stroke="currentColor"
                             stroke-width="2"
                             stroke-linecap="round"
                             stroke-linejoin="round">
                            <path
                                  d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4">
                            </path>
                            <polyline
                                      points="17 8 12 3 7 8">
                            </polyline>
                            <line x1="12" y1="3" x2="12"
                                  y2="15"></line>
                        </svg>
                    </div>
                    <p class="upload-text">Drag and drop
                        your file here or</p>
                    <label class="btn btn-primary">
                        Browse Files
                        <input type="file" ref="fileInput"
                               @change="handleFileChange"
                               accept=".csv,.json"
                               class="file-input" />
                    </label>
                    <p class="supported-formats">Supported
                        formats: CSV, JSON</p>
                </div>
            </div>

            <div v-if="selectedFile" class="selected-file">
                <div class="file-info">
                    <svg xmlns="http://www.w3.org/2000/svg"
                         viewBox="0 0 24 24" width="24"
                         height="24" fill="none"
                         stroke="currentColor"
                         stroke-width="2"
                         stroke-linecap="round"
                         stroke-linejoin="round">
                        <path
                              d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z">
                        </path>
                        <polyline points="14 2 14 8 20 8">
                        </polyline>
                        <line x1="16" y1="13" x2="8"
                              y2="13"></line>
                        <line x1="16" y1="17" x2="8"
                              y2="17"></line>
                        <polyline points="10 9 9 9 8 9">
                        </polyline>
                    </svg>
                    <div class="file-details">
                        <span class="file-name">{{
                            selectedFile.name }}</span>
                        <span class="file-size">{{
                            formatFileSize(selectedFile.size)
                            }}</span>
                    </div>
                </div>
                <button @click="clearFile"
                        class="btn btn-danger btn-sm">Remove</button>
            </div>

            <button v-if="selectedFile" @click="uploadFile"
                    class="btn btn-primary upload-button"
                    :disabled="loading">
                {{ loading ? 'Uploading...' : 'Upload File'
                }}
            </button>
        </div>

        <div v-if="error" class="error-message">
            {{ error }}
        </div>

        <div v-if="loading" class="loading-container">
            <div class="spinner"></div>
            <p>Uploading file...</p>
        </div>

        <div v-if="fileAnalysis" class="file-analysis">
            <h2>File Analysis</h2>

            <div class="analysis-card">
                <div class="analysis-header">
                    <h3>{{ fileAnalysis.filename }}</h3>
                    <span class="file-type-badge"
                          :class="fileAnalysis.file_type">
                        {{
                            fileAnalysis.file_type.toUpperCase()
                        }}
                    </span>
                </div>

                <div class="analysis-stats">
                    <div class="stat-item">
                        <span
                              class="stat-label">Rows:</span>
                        <span class="stat-value">{{
                            fileAnalysis.row_count }}</span>
                    </div>

                    <div class="stat-item">
                        <span
                              class="stat-label">Columns:</span>
                        <span class="stat-value">{{
                            fileAnalysis.column_count
                            }}</span>
                    </div>
                </div>

                <div class="analysis-section">
                    <h4>Columns</h4>
                    <div class="columns-list">
                        <div v-for="(colType, colName) in fileAnalysis.column_types"
                             :key="colName"
                             class="column-item">
                            <span class="column-name">{{
                                colName }}</span>
                            <span class="column-type">{{
                                colType }}</span>
                        </div>
                    </div>
                </div>

                <div class="analysis-section">
                    <h4>Sample Data</h4>
                    <div class="table-responsive">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th v-for="column in fileAnalysis.columns"
                                        :key="column">
                                        {{ column }}
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(row, rowIndex) in fileAnalysis.sample_rows"
                                    :key="rowIndex">
                                    <td v-for="column in fileAnalysis.columns"
                                        :key="column">
                                        {{ row[column] }}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'FileUploader',
    data() {
        return {
            selectedFile: null,
            isDragOver: false,
            loading: false,
            error: '',
            fileAnalysis: null
        };
    },
    methods: {
        handleDragOver(event) {
            this.isDragOver = true;
        },

        handleDragLeave(event) {
            this.isDragOver = false;
        },

        handleDrop(event) {
            this.isDragOver = false;

            if (event.dataTransfer.files.length > 0) {
                const file = event.dataTransfer.files[0];
                this.validateAndSetFile(file);
            }
        },

        handleFileChange(event) {
            if (event.target.files.length > 0) {
                const file = event.target.files[0];
                this.validateAndSetFile(file);
            }
        },

        validateAndSetFile(file) {
            // Check file type
            const validTypes = ['.csv', '.json', 'text/csv', 'application/json'];
            const fileExt = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();

            if (validTypes.includes(fileExt) || validTypes.includes(file.type)) {
                this.selectedFile = file;
                this.error = '';
            } else {
                this.error = 'Invalid file type. Please upload a CSV or JSON file.';
            }
        },

        clearFile() {
            this.selectedFile = null;
            this.fileAnalysis = null;
            this.$refs.fileInput.value = '';
        },

        formatFileSize(bytes) {
            if (bytes < 1024) {
                return bytes + ' bytes';
            } else if (bytes < 1024 * 1024) {
                return (bytes / 1024).toFixed(1) + ' KB';
            } else {
                return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
            }
        },

        async uploadFile() {
            if (!this.selectedFile) return;

            this.loading = true;
            this.error = '';
            this.fileAnalysis = null;

            try {
                // Create form data
                const formData = new FormData();
                formData.append('file', this.selectedFile);

                // Use API URL from environment variable or default
                const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

                // Upload the file
                const response = await fetch(`${apiUrl}/api/data/upload`, {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || `Upload failed with status ${response.status}`);
                }

                // Get the analysis result
                this.fileAnalysis = await response.json();
                console.log('File analysis:', this.fileAnalysis);
            } catch (err) {
                console.error('Error uploading file:', err);
                this.error = err.message || 'Failed to upload file';
            } finally {
                this.loading = false;
            }
        }
    }
};
</script>
