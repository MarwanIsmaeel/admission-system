<template>
  <div class="max-w-2xl mx-auto py-8 text-right" dir="rtl">
    <div class="bg-white p-8 rounded-lg shadow-sm border border-gray-200">
      <h1 class="text-2xl font-bold text-gray-900 mb-6 border-b pb-4 text-center">تعليمات التقديم والقبول المركزي</h1>
      
      <div class="space-y-6 text-gray-700 leading-relaxed mb-8">
        <section>
          <h3 class="font-bold text-indigo-700 mb-2">1. متطلبات عامة:</h3>
          <ul class="list-disc list-inside pr-4 space-y-2">
            <li>يجب أن يكون الطالب من خريجي الدراسة الإعدادية للعام الدراسي الحالي.</li>
            <li>يجب إدخال كافة البيانات الشخصية بدقة كما هي واردة في الهوية الرسمية.</li>
            <li>رقم الهاتف المدخل يجب أن يكون فعالاً لاستلام الإشعارات.</li>
          </ul>
        </section>

        <section>
          <h3 class="font-bold text-indigo-700 mb-2">2. القيود الأكاديمية:</h3>
          <ul class="list-disc list-inside pr-4 space-y-2">
            <li>الحد الأدنى للمعدل المسموح به للتقديم هو 50%.</li>
            <li>يجب إدخال الرقم الامتحاني الفريد الخاص بك بشكل صحيح.</li>
            <li>لا يمكن تعديل البيانات بعد إرسال الاستمارة النهائية.</li>
          </ul>
        </section>

        <section>
          <h3 class="font-bold text-indigo-700 mb-2">3. الوثائق المطلوبة:</h3>
          <ul class="list-disc list-inside pr-4 space-y-2">
            <li>يجب رفع نسخة واضحة من الوثائق المدرسية أو الهوية الرسمية (بصيغة PDF أو صورة).</li>
            <li>أي تلاعب في البيانات أو الوثائق المرفوعة يعرض الطالب للمساءلة القانونية وإلغاء القبول.</li>
          </ul>
        </section>

        <div class="bg-yellow-50 border-r-4 border-yellow-400 p-4 mt-6">
          <p class="text-sm text-yellow-800 font-bold">
            تنبيه: لا تقم بمشاركة رمز التفعيل الخاص بك مع أي شخص آخر، حيث يمكن استخدامه لتقديم طلب واحد فقط.
          </p>
        </div>
      </div>

      <div class="border-t pt-6">
        <label class="flex items-center cursor-pointer">
          <input 
            type="checkbox" 
            v-model="acknowledged" 
            class="h-5 w-5 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
          >
          <span class="mr-3 text-gray-900 font-bold">لقد قرأت كافة التعليمات المذكورة أعلاه وأوافق على الالتزام بها.</span>
        </label>

        <button 
          @click="proceedToVoucher"
          :disabled="!acknowledged"
          class="w-full mt-8 flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-lg font-bold text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 transition-all duration-200"
        >
          الانتقال إلى إدخال رمز التفعيل
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const acknowledged = ref(false);
const router = useRouter();

const proceedToVoucher = () => {
  if (acknowledged.value) {
    router.push('/voucher');
  }
};
</script>
