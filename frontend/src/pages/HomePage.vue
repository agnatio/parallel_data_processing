<template>
  <div class="container mx-auto px-1 py-1 flex">
    <!-- Data Generators Grid (moved to the left) -->
    <div
         class="w-3/4 grid grid-cols-1 md:grid-cols-2 gap-2">
      <DataGenerator :rows="10" :columns="5"
                     name="Generator 1"
                     @generation-start="addToQueue"
                     @generation-complete="markAsComplete" />
      <DataGenerator :rows="20" :columns="8"
                     name="Generator 2"
                     @generation-start="addToQueue"
                     @generation-complete="markAsComplete" />
      <DataGenerator :rows="15" :columns="10"
                     name="Generator 3"
                     @generation-start="addToQueue"
                     @generation-complete="markAsComplete" />
      <DataGenerator :rows="5" :columns="3"
                     name="Generator 4"
                     @generation-start="addToQueue"
                     @generation-complete="markAsComplete" />
    </div>

    <!-- Queue Visualization (on the right) -->
    <div class="w-1/4 ml-4 bg-gray-100 rounded-lg p-4">
      <h3 class="text-lg font-medium mb-4">Processing Queue
      </h3>
      <div class="space-y-2">
        <div v-if="queueItems.length === 0"
             class="text-gray-500 text-sm italic">
          No active tasks
        </div>
        <div v-for="(item, index) in queueItems"
             :key="index"
             class="border rounded-md p-2 transition-all duration-300"
             :class="{
              'bg-blue-100 border-blue-300': item.status === 'processing',
              'bg-green-100 border-green-300': item.status === 'completed'
            }">
          <div class="flex justify-between items-center">
            <span class="font-medium">{{ item.name }}</span>
            <span class="text-xs px-2 py-1 rounded" :class="{
              'bg-blue-500 text-white': item.status === 'processing',
              'bg-green-500 text-white': item.status === 'completed'
            }">
              {{ item.status === 'processing' ? 'Processing'
                : 'Completed' }}
            </span>
          </div>

          <!-- Progress bar -->
          <div v-if="item.status === 'processing'"
               class="w-full bg-gray-200 rounded-full h-2.5 mt-2">
            <div class="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
                 :style="{ width: `${item.progress}%` }">
            </div>
          </div>

          <div v-if="item.status === 'processing'"
               class="text-xs text-gray-500 mt-1">
            Est. time: {{ item.expectedDuration }}s
          </div>

          <div v-if="item.status === 'completed'"
               class="text-xs text-green-600 mt-1">
            Completed in {{ item.actualDuration.toFixed(1)
            }}s
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import DataGenerator from '@/components/DataGenerator.vue';

// Queue state
const queueItems = ref([]);

// Add item to processing queue
function addToQueue(name, expectedDuration) {
  const item = {
    id: Date.now().toString(),
    name: name,
    status: 'processing',
    startTime: Date.now(),
    progress: 0,
    expectedDuration: expectedDuration,
    actualDuration: 0
  };

  queueItems.value.push(item);

  // Start updating progress
  updateProgress(item.id, expectedDuration);
}

// Update progress percentage
function updateProgress(id, duration) {
  const intervalTime = 100; // Update every 100ms
  const steps = duration * 1000 / intervalTime;
  let currentStep = 0;

  const interval = setInterval(() => {
    const itemIndex = queueItems.value.findIndex(item => item.id === id);
    if (itemIndex === -1 || queueItems.value[itemIndex].status === 'completed') {
      clearInterval(interval);
      return;
    }

    currentStep++;
    const progress = Math.min((currentStep / steps) * 100, 99.5); // Cap at 99.5% until complete
    queueItems.value[itemIndex].progress = progress;

    // Auto-complete after expected duration + buffer
    if (currentStep >= steps * 1.5) {
      clearInterval(interval);
      // Only mark as complete if it wasn't already completed
      if (queueItems.value[itemIndex].status === 'processing') {
        markAsComplete(queueItems.value[itemIndex].name);
      }
    }
  }, intervalTime);
}

// Mark task as complete
function markAsComplete(name) {
  const itemIndex = queueItems.value.findIndex(item => item.name === name && item.status === 'processing');
  if (itemIndex !== -1) {
    const item = queueItems.value[itemIndex];
    item.status = 'completed';
    item.progress = 100;
    item.actualDuration = (Date.now() - item.startTime) / 1000;

    // Remove from queue after 5 seconds
    setTimeout(() => {
      const currentIndex = queueItems.value.findIndex(i => i.id === item.id);
      if (currentIndex !== -1) {
        queueItems.value.splice(currentIndex, 1);
      }
    }, 5000);
  }
}

// Clean up old tasks on mount
onMounted(() => {
  // Clear any leftover tasks
  queueItems.value = [];
});
</script>