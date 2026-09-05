<template>

       <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4" dir="rtl">
            <div class="text-center">
                      <h1 class="text-7xl font-bold text-gray-800">404</h1>
                      <h2 class="mt-4 text-2xl font-bold text-gray-800">
                        الصفحة غير موجودة
                    </h2>

                    <p class="mt-3 text-gray-600">
                        عذراً، الصفحة التي تحاول الوصول إليها غير موجودة أو تم إيقافها.
                    </p>

                    <router-link
                        to="/"
                        class="inline-block mt-6 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                    >
                        العودة إلى الصفحة الرئيسية
                    </router-link>
            </div>
        </div>
</template>

