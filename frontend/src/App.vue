<template>
  <div class="min-h-screen bg-gray-50 flex flex-col" dir="rtl">
    <!-- Updated Navbar Color -->
    <nav class="bg-slate-900 shadow-md" dir="rtl">
    <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16 sm:h-20 gap-2">
        
      <!-- Right Side: Responsive Title -->
      <router-link 
        to="/" 
        class="flex items-center text-white text-xs sm:text-lg md:text-xl font-bold leading-tight min-w-0"
      >
        <span class="truncate sm:whitespace-normal">
          نظام التقديم للدراسة المسائية / جامعة النهرين / كلية الهندسة
        </span>
      </router-link>

      <!-- Left Side: Responsive Circular Logo -->
      <div class="flex-shrink-0">
        <img 
          src="./assets/logo.jpg" 
          alt="شعار كلية الهندسة" 
          class="h-8 w-8 sm:h-11 sm:w-11 md:h-12 md:w-12 rounded-full object-cover border-2 border-indigo-400"
        />
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
        <div class="flex flex-col md:flex-row justify-center items-center space-y-4 md:space-y-0">
          <div class="text-gray-400 text-md text-center font-medium tracking-wide">
            All Rights Reserved &copy; {{ new Date().getFullYear() }} College of Engineering
          </div>
          <!-- <div class="flex items-center space-x-6 text-sm text-gray-400 font-semibold  tracking-widest">
            <span>AL-Nahrain University</span>
          </div> -->
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
