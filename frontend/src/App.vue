<template>
  <div class="min-h-screen bg-gray-50 flex flex-col" dir="rtl">
    <!-- Updated Navbar Color -->
    <nav class="bg-slate-900 shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <router-link to="/" class="flex-shrink-0 flex items-center  text-white text-xl">
              نظام إدارة التقديم للدراسة المسائية
            </router-link>
            <div class="hidden sm:-my-px sm:mr-10 sm:flex sm:space-x-reverse sm:space-x-8">
              <router-link 
                to="/" 
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition"
                :class="$route.path === '/' ? 'border-indigo-400 text-white' : 'border-transparent text-gray-300 hover:text-white hover:border-gray-300'"
              >
                الرئيسية
              </router-link>
              <router-link 
                to="/status" 
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition"
                :class="$route.path === '/status' ? 'border-indigo-400 text-white' : 'border-transparent text-gray-300 hover:text-white hover:border-gray-300'"
              >
                استعلام عن حالة القبول
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main content takes available space -->
    <main class="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8 font-arabic flex-grow w-full">
      <router-view />
    </main>

    <!-- Professional Dark Footer -->
    <footer class="bg-slate-900 border-t border-slate-800 py-8 mt-auto" dir="ltr">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          <div class="text-gray-400 text-sm font-medium tracking-wide">
            &copy; {{ new Date().getFullYear() }} COLLEGE OF ENGINEERING. ALL RIGHTS RESERVED.
          </div>
          <div class="flex items-center space-x-6 text-sm text-gray-400 font-semibold uppercase tracking-widest">
            <span>AL-NAHRAIN UNIVERSITY</span>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
</script>

<style>
/* Base styles */
</style>
