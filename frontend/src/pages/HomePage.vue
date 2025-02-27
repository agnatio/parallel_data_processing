<template>
  <div class="home-page">

    <div class="tab-content">
      <DataGenerator v-if="activeTab === 'generator'" />
    </div>
  </div>
</template>

<script>
import DataGenerator from '@/components/DataGenerator.vue';

export default {
  name: 'HomePage',
  components: {
    DataGenerator,
  },
  data() {
    return {
      activeTab: 'generator'
    };
  }
};
</script>