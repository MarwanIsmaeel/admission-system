<template>
  <div class="max-w-md mx-auto text-right">
    <h1 class="text-3xl font-bold mb-6 text-center text-gray-900">استعلام عن حالة القبول</h1>
    <div class="bg-white p-8 rounded-lg shadow-sm border border-gray-200">
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-1">أدخل رمز </label>
        <input 
          v-model="code" 
          type="text" 
          placeholder="ENG-XXXXXX"
          class="w-full border p-2 rounded focus:ring-indigo-500 focus:border-indigo-500 text-center font-mono"
        >
      </div>
      <button 
        @click="checkStatus"
        :disabled="loading"
        class="w-full bg-indigo-600 text-white py-2 rounded font-bold hover:bg-indigo-700 transition disabled:opacity-50"
      >
        {{ loading ? 'جاري البحث...' : 'بحث' }}
      </button>
      
      <div v-if="error" class="mt-4 p-3 bg-red-50 text-red-700 rounded text-sm font-bold">
        {{ error }}
      </div>

      <div v-if="result" class="mt-6 p-6 bg-indigo-50 rounded-lg border border-indigo-100">
        <h3 class="font-bold text-indigo-900 mb-4 border-b border-indigo-200 pb-2">تفاصيل الطلب:</h3>
        <div class="space-y-3">
          <p><span class="text-indigo-700 font-medium">الاسم:</span> <span class="text-gray-900">{{ result.full_name }}</span></p>
          <p>
            <span class="text-indigo-700 font-medium">الحالة:</span> 
            <span :class="statusClass" class="px-2 py-1 rounded text-xs font-bold mr-2">
              {{ translateStatus(result.status) }}
            </span>
          </p>
          <p>
            <span class="text-indigo-700 font-medium">القسم المقبول فيه:</span> 
            <span class="text-gray-900 font-bold">{{ result.assigned_dept_name || 'لم يتم التخصيص بعد' }}</span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import api from '../api';

const code = ref('');
const result = ref(null);
const loading = ref(false);
const error = ref('');

const checkStatus = async () => {
  if (!code.value) return;
  
  loading.value = true;
  error.value = '';
  result.value = null;
  
  try {
    const response = await api.get('check-status/', { params: { code: code.value } });
    result.value = response.data;
  } catch (err) {
    error.value = 'لم يتم العثور على طلب لهذا الرمز. تأكد من إدخال الرمز بشكل صحيح.';
  } finally {
    loading.value = false;
  }
};

const translateStatus = (status) => {
  const map = {
    'submitted': 'تم التقديم',
    'pending': 'قيد المعالجة',
    'accepted': 'تم القبول',
    'rejected': 'مرفوض',
    'not_allocated': 'لم يحصل على قبول',
    'draft': 'مسودة'
  };
  return map[status] || status;
};

const statusClass = computed(() => {
  if (!result.value) return '';
  const s = result.value.status;
  if (s === 'accepted') return 'bg-green-100 text-green-800';
  if (s === 'rejected' || s === 'not_allocated') return 'bg-red-100 text-red-800';
  return 'bg-blue-100 text-blue-800';
});
</script>
