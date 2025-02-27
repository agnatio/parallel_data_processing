<template>
    <div class="bg-gray-50 p-4 rounded-lg w-full h-full">
        <!-- Container with fixed height to prevent layout shifts -->
        <div class="h-96 overflow-hidden flex flex-col">
            <!-- Error display -->
            <div v-if="error"
                 class="p-4 mb-4 bg-red-100 border border-red-400 text-red-700 rounded">
                {{ error }}
            </div>

            <!-- Loading state -->
            <div v-if="isLoading"
                 class="flex flex-col items-center justify-center flex-grow">
                <div
                     class="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin">
                </div>
                <p class="mt-4 text-gray-600">Generating
                    data...</p>
            </div>

            <!-- No data state -->
            <div v-else-if="!hasData"
                 class="flex flex-col items-center justify-center flex-grow text-gray-500">
                <p>No data generated yet</p>
                <p class="text-sm mt-2">Use the form to
                    generate data</p>
            </div>

            <!-- JSON Data Preview -->
            <div v-else-if="format === 'json' && jsonData"
                 class="space-y-4 flex-grow flex flex-col">
                <h2
                    class="text-xl font-semibold text-gray-800">
                    JSON Preview</h2>
                <div
                     class="flex space-x-4 text-sm text-gray-600">
                    <span><strong>Rows:</strong> {{
                        jsonData.metadata.rows }}</span>
                    <span><strong>Columns:</strong> {{
                        jsonData.metadata.columns }}</span>
                </div>

                <div
                     class="overflow-auto border border-gray-200 rounded flex-grow">
                    <table
                           class="min-w-full divide-y divide-gray-200">
                        <thead
                               class="bg-gray-100 sticky top-0">
                            <tr>
                                <th v-for="(header, index) in jsonData.metadata.headers"
                                    :key="index"
                                    class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    {{ header }}
                                </th>
                            </tr>
                        </thead>
                        <tbody
                               class="bg-white divide-y divide-gray-200">
                            <tr v-for="(row, rowIndex) in jsonPreviewData"
                                :key="rowIndex">
                                <td v-for="(column, columnIndex) in jsonData.metadata.headers"
                                    :key="columnIndex"
                                    class="px-4 py-2 text-sm text-gray-600 whitespace-nowrap">
                                    {{ row[column] }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- CSV Data Preview -->
            <div v-else-if="format === 'csv' && csvData"
                 class="space-y-4 flex-grow flex flex-col">
                <h2
                    class="text-xl font-semibold text-gray-800">
                    CSV Preview</h2>

                <div
                     class="overflow-auto border border-gray-200 rounded flex-grow">
                    <table
                           class="min-w-full divide-y divide-gray-200">
                        <thead
                               class="bg-gray-100 sticky top-0">
                            <tr>
                                <th v-for="(header, index) in csvHeaders"
                                    :key="index"
                                    class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    {{ header }}
                                </th>
                            </tr>
                        </thead>
                        <tbody
                               class="bg-white divide-y divide-gray-200">
                            <tr v-for="(row, rowIndex) in csvRows"
                                :key="rowIndex">
                                <td v-for="(cell, cellIndex) in row"
                                    :key="cellIndex"
                                    class="px-4 py-2 text-sm text-gray-600 whitespace-nowrap">
                                    {{ cell }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    jsonData: {
        type: Object,
        default: null
    },
    csvData: {
        type: String,
        default: null
    },
    format: {
        type: String,
        default: 'json',
        validator: (value) => ['json', 'csv'].includes(value)
    },
    isLoading: {
        type: Boolean,
        default: false
    },
    error: {
        type: String,
        default: ''
    }
});

// Computed property to check if we have any data to display
const hasData = computed(() => {
    return (props.format === 'json' && props.jsonData) ||
        (props.format === 'csv' && props.csvData);
});

// JSON data computations
const jsonPreviewData = computed(() => {
    if (props.jsonData && props.jsonData.data) {
        // Return up to 5 rows for preview
        return props.jsonData.data.slice(0, 5);
    }
    return [];
});

// CSV data computations
const csvHeaders = computed(() => {
    if (props.csvData) {
        const lines = props.csvData.split('\n');
        if (lines.length > 0) {
            return parseCsvLine(lines[0]);
        }
    }
    return [];
});

const csvRows = computed(() => {
    if (props.csvData) {
        const lines = props.csvData.split('\n');
        if (lines.length > 1) {
            // Return up to 5 rows for preview
            return lines.slice(1, 6)
                .filter(line => line.trim().length > 0)
                .map(line => parseCsvLine(line));
        }
    }
    return [];
});

// Helper function for parsing CSV lines
function parseCsvLine(line) {
    // Basic CSV parsing (not handling quoted values properly for brevity)
    return line.split(',').map(field => field.trim());
}
</script>