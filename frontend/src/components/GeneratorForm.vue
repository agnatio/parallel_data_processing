<template>
    <div class="bg-gray-50 p-4 rounded-lg w-full h-full">
        <div class="space-y-4">
            <div class="space-y-2">
                <label for="rows"
                       class="block text-sm font-medium text-gray-700">Rows:</label>
                <input id="rows"
                       v-model.number="formData.rows"
                       type="number" min="1" max="1000"
                       class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" />
            </div>

            <div class="space-y-2">
                <label for="columns"
                       class="block text-sm font-medium text-gray-700">Columns:</label>
                <input id="columns"
                       v-model.number="formData.columns"
                       type="number" min="1" max="20"
                       class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" />
            </div>

            <div class="space-y-2">
                <label for="format"
                       class="block text-sm font-medium text-gray-700">Output
                    Format:</label>
                <select id="format"
                        v-model="formData.format"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                    <option value="json">JSON</option>
                    <option value="csv">CSV</option>
                </select>
            </div>

            <div class="flex flex-col space-y-3 pt-4">
                <button @click="handleGenerate"
                        class="w-full px-4 py-2 bg-indigo-600 text-white font-medium rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                        :disabled="isLoading">
                    {{ isLoading ? 'Generating...' :
                        'Generate Data' }}
                </button>

                <button @click="handleDownload"
                        class="w-full px-4 py-2 bg-green-600 text-white font-medium rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
                        :disabled="isLoading || !hasGeneratedData">
                    Download {{
                        formData.format.toUpperCase() }}
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, watch, toRefs } from 'vue';

const props = defineProps({
    isLoading: {
        type: Boolean,
        default: false
    },
    hasGeneratedData: {
        type: Boolean,
        default: false
    },
    initialRows: {
        type: Number,
        default: 10
    },
    initialColumns: {
        type: Number,
        default: 10
    },
    initialFormat: {
        type: String,
        default: 'json'
    }
});

const emit = defineEmits([
    'generate',
    'download',
    'update:rows',
    'update:columns',
    'update:format'
]);

// Form state using reactive for better organization
const formData = reactive({
    rows: props.initialRows,
    columns: props.initialColumns,
    format: props.initialFormat
});

// Watch for changes to emit updates
watch(() => formData.rows, (newValue) => {
    emit('update:rows', newValue);
});

watch(() => formData.columns, (newValue) => {
    emit('update:columns', newValue);
});

watch(() => formData.format, (newValue) => {
    emit('update:format', newValue);
});

// Handler functions
function handleGenerate() {
    emit('generate', {
        rows: formData.rows,
        columns: formData.columns,
        format: formData.format
    });
}

function handleDownload() {
    emit('download', {
        rows: formData.rows,
        columns: formData.columns,
        format: formData.format
    });
}
</script>