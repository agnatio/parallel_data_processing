<template>
  <div class="home-page">
    <h1>Data Generation Tool</h1>
    <p>Generate CSV and JSON data for testing and development</p>
    
    <div class="tabs">
      <button 
        @click="activeTab = 'generator'"
        :class="{ active: activeTab === 'generator' }"
      >
        Data Generator
      </button>
      <button 
        @click="activeTab = 'uploader'"
        :class="{ active: activeTab === 'uploader' }"
      >
        File Uploader
      </button>
    </div>
    
    <div class="tab-content">
      <DataGenerator v-if="activeTab === 'generator'" />
      <FileUploader v-if="activeTab === 'uploader'" />
    </div>
  </div>
</template>

<script>
import DataGenerator from '@/components/DataGenerator.vue';
import FileUploader from '@/components/FileUploader.vue';

export default {
  name: 'HomePage',
  components: {
    DataGenerator,
    FileUploader
  },
  data() {
    return {
      activeTab: 'generator'
    };
  }
};
</script>