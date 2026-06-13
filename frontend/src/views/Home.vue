<template>
  <div class="max-w-md mx-auto bg-white p-8 border border-gray-200 rounded-lg shadow-sm">
    <h2 class="text-2xl font-bold text-gray-900 mb-6 text-right">أدخل رمز التفعيل</h2>
    <form @submit.prevent="verifyVoucher">
      <div class="mb-4">
        <label for="code" class="block text-sm font-medium text-gray-700 text-right">رمز التفعيل</label>
        <input 
          v-model="code" 
          type="text" 
          id="code" 
          placeholder="ENG-XXXXXX"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm text-center font-mono"
          required
        >
      </div>
      <div v-if="error" class="mb-4 text-red-600 text-sm text-right font-bold">
        {{ error }}
      </div>
      <button 
        type="submit" 
        :disabled="loading"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
      >
        {{ loading ? 'جاري التحقق...' : 'الاستمرار في التقديم' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';
import { useAuthStore } from '../stores/auth';

const code = ref('');
const error = ref('');
const loading = ref(false);
const router = useRouter();
const auth = useAuthStore();

const verifyVoucher = async () => {
  loading.value = true;
  error.value = '';
  try {
    const response = await api.post('verify-voucher/', { code: code.value });
    auth.setVoucher(code.value, response.data);
    router.push('/apply');
  } catch (err) {
    if (err.response?.status === 429) {
        error.value = err.response.data.error; // Show the backend's "Too many attempts" message
    } else if (err.response?.status === 404) {
        error.value = 'رمز التفعيل غير صحيح';
    } else if (err.response?.data?.error) {
        // Handle specific "already used" message
        error.value = err.response.data.error === 'This voucher is already used' ? 'هذا الرمز مستخدم بالفعل' : err.response.data.error;
    } else {
        error.value = 'تعذر التحقق من الرمز. يرجى المحاولة لاحقاً';
    }
  } finally {

    loading.value = false;
  }
};
</script>
