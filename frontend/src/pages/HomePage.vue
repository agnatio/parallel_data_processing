<template>
  <div class="container mx-auto px-1 py-1">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
      <DataGenerator />
      <DataGenerator />
      <DataGenerator />
      <DataGenerator />
    </div>
  </div>
</template>

<script setup>
import DataGenerator from '@/components/DataGenerator.vue';
</script>