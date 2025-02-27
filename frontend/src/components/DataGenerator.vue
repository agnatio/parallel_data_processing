<template>
    <div class="max-w-2xl mx-auto px-2 py-2">

        <div
             class="grid grid-cols-1 lg:grid-cols-3 gap-2 bg-white rounded-lg shadow-lg p-6 h-[500px]">
            <!-- Form Section -->
            <div class="lg:col-span-1 h-full">
                <GeneratorForm :is-loading="loading"
                               :has-generated-data="hasGeneratedData"
                               :initial-rows="rows"
                               :initial-columns="columns"
                               :initial-format="selectedFormat"
                               @generate="generateData"
                               @download="downloadData"
                               @update:rows="rows = $event"
                               @update:columns="columns = $event"
                               @update:format="handleFormatChange" />
            </div>

            <!-- Preview Section -->
            <div class="lg:col-span-2 h-full">
                <DataPreview :json-data="jsonData"
                             :csv-data="csvData"
                             :format="selectedFormat"
                             :is-loading="loading"
                             :error="error" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import GeneratorForm from './GeneratorForm.vue';
import DataPreview from './DataPreview.vue';
import { dataService } from '@/services/apiClient';

// Form inputs
const rows = ref(10);
const columns = ref(10);
const selectedFormat = ref('json');
const selectedDataTypes = ref([]);

// Data state
const jsonData = ref(null);
const csvData = ref(null);
const loading = ref(false);
const error = ref('');

// Computed properties
const hasGeneratedData = computed(() => {
    return (selectedFormat.value === 'json' && jsonData.value) ||
        (selectedFormat.value === 'csv' && csvData.value);
});

// Watch for column changes to adjust data types
watch(columns, (newValue) => {
    if (selectedDataTypes.value.length > newValue) {
        selectedDataTypes.value = selectedDataTypes.value.slice(0, newValue);
    }
});

// Methods
function handleFormatChange(newFormat) {
    // Clear data when format changes
    if (newFormat === 'json') {
        csvData.value = null;
    } else {
        jsonData.value = null;
    }
    selectedFormat.value = newFormat;
}

async function generateData(formData) {
    loading.value = true;
    error.value = '';

    try {
        // Use the form data or fall back to component state
        const requestRows = formData?.rows || rows.value;
        const requestColumns = formData?.columns || columns.value;
        const requestFormat = formData?.format || selectedFormat.value;

        // Prepare parameters for the API call
        const params = {
            rows: requestRows,
            columns: requestColumns,
            format: requestFormat
        };

        // Use the dataService to make the API call
        const response = await dataService.generateData(params);

        // Process based on selected format
        if (requestFormat === 'json') {
            jsonData.value = response.data;
            csvData.value = null;
        } else {
            // For CSV, the response will be text
            csvData.value = response.data;
            jsonData.value = null;
        }
    } catch (err) {
        console.error('Error generating data:', err);
        error.value = err.response?.data?.detail || err.message || 'Failed to generate data';
    } finally {
        loading.value = false;
    }
}

async function downloadData(formData) {
    if (!hasGeneratedData.value) return;

    try {
        // Use the form data or fall back to component state
        const requestRows = formData?.rows || rows.value;
        const requestColumns = formData?.columns || columns.value;
        const requestFormat = formData?.format || selectedFormat.value;

        // Prepare parameters for the URL
        const params = new URLSearchParams();
        params.append('rows', requestRows);
        params.append('columns', requestColumns);
        params.append('format', requestFormat);

        // Get base URL from environment or default
        const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

        // Create download URL
        const downloadUrl = `${baseURL}/api/data/generate?${params.toString()}`;

        // Create an anchor element and trigger download
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = `generated_data_${requestRows}x${requestColumns}.${requestFormat}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    } catch (err) {
        console.error('Error downloading data:', err);
        error.value = err.message || 'Failed to download data';
    }
}
</script>