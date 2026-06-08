<template>
  <div class="max-w-md mx-auto py-12 text-center" dir="rtl">
    <div class="bg-white p-8 rounded-lg shadow-sm border border-gray-200">
      <div class="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-6">
        <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>
      </div>
      
      <h2 class="text-2xl font-bold text-gray-900 mb-2">تم إرسال الطلب بنجاح!</h2>
      <p class="text-gray-600 mb-8">
        لقد تم استلام طلب التقديم الخاص بك بنجاح. يمكنك الآن متابعة حالة طلبك باستخدام رمز القسيمة الخاص بك.
      </p>
      
      <div class="space-y-4">
        <router-link 
          to="/status" 
          class="block w-full py-2 px-4 bg-indigo-600 text-white font-bold rounded-md hover:bg-indigo-700 transition"
        >
          الاستعلام عن الحالة الآن
        </router-link>
        
        <router-link 
          to="/" 
          class="block w-full py-2 px-4 bg-gray-100 text-gray-700 font-bold rounded-md hover:bg-gray-200 transition"
        >
          العودة للصفحة الرئيسية
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>
