<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">Dashboard</h1>
    <div v-if="stats" class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <p class="text-gray-500 text-sm">Total Applications</p>
        <p class="text-2xl font-bold">{{ stats.total_applications }}</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <p class="text-gray-500 text-sm">Accepted</p>
        <p class="text-2xl font-bold text-green-600">{{ stats.accepted }}</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <p class="text-gray-500 text-sm">Rejected</p>
        <p class="text-2xl font-bold text-red-600">{{ stats.rejected }}</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <p class="text-gray-500 text-sm">Not Allocated</p>
        <p class="text-2xl font-bold text-orange-600">{{ stats.not_allocated }}</p>
      </div>
    </div>
    
    <div v-if="stats" class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h3 class="text-lg font-bold mb-4">Department Statistics</h3>
      <table class="min-w-full">
        <thead>
          <tr class="text-left border-b">
            <th class="pb-2">Department</th>
            <th class="pb-2 text-center">Capacity</th>
            <th class="pb-2 text-center">Assigned</th>
            <th class="pb-2 text-center">Remaining</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="dept in stats.department_stats" :key="dept.name" class="border-b last:border-0">
            <td class="py-3">{{ dept.name }}</td>
            <td class="py-3 text-center">{{ dept.capacity }}</td>
            <td class="py-3 text-center">{{ dept.assigned }}</td>
            <td class="py-3 text-center">{{ dept.remaining }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';

const stats = ref(null);

onMounted(async () => {
  try {
    const response = await api.get('dashboard-stats/');
    stats.value = response.data;
  } catch (err) {
    console.error('Failed to fetch stats');
  }
});
</script>
