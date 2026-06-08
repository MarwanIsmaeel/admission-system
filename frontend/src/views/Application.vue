<template>
  <div class="max-w-4xl mx-auto pb-12 text-right">
    <div v-if="!auth.voucherCode" class="text-center py-12 bg-white rounded-lg shadow-sm border">
      <p class="text-red-500 mb-4">لا توجد جلسة نشطة. يرجى التحقق من القسيمة أولاً.</p>
      <router-link to="/" class="text-indigo-600 font-bold hover:underline">العودة للرئيسية</router-link>
    </div>

    <div v-else-if="loadingInitial" class="text-center py-12">
      <p class="text-gray-500">جاري تحميل البيانات...</p>
    </div>

    <div v-else-if="!currentRound" class="text-center py-12 bg-white rounded-lg shadow-sm border px-6">
      <h2 class="text-2xl font-bold text-gray-900 mb-2">التقديم مغلق</h2>
      <p class="text-gray-600">لا توجد دورة قبول نشطة في الوقت الحالي.</p>
    </div>

    <div v-else>
      <div class="mb-8 flex justify-between items-end flex-row-reverse">
        <div class="text-right">
          <h1 class="text-3xl font-bold text-gray-900">استمارة التقديم الإلكتروني</h1>
          <p class="text-gray-600 mt-1">الرمز: <span class="font-mono font-bold text-indigo-600">{{ auth.voucherCode }}</span></p>
        </div>
        <div class="text-left">
          <p class="text-sm text-gray-500">الدورة الحالية</p>
          <p class="font-bold text-gray-900">{{ currentRound.name }}</p>
        </div>
      </div>

      <form @submit.prevent="submitApplication" class="space-y-8">
        <!-- 1. Personal Information -->
        <section class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 class="text-lg font-bold text-gray-900 mb-4 pb-2 border-b">المعلومات الشخصية</h3>
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">الاسم الأول <span class="text-red-500">*</span></label>
              <input v-model="form.first_name" type="text" required class="mt-1 block w-full border rounded-md p-2 shadow-sm focus:ring-indigo-500 focus:border-indigo-500">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">الاسم الثاني <span class="text-red-500">*</span></label>
              <input v-model="form.second_name" type="text" required class="mt-1 block w-full border rounded-md p-2 shadow-sm">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">الاسم الثالث <span class="text-red-500">*</span></label>
              <input v-model="form.third_name" type="text" required class="mt-1 block w-full border rounded-md p-2 shadow-sm">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">الاسم الرابع <span class="text-red-500">*</span></label>
              <input v-model="form.fourth_name" type="text" required class="mt-1 block w-full border rounded-md p-2 shadow-sm">
            </div>
          </div>
          <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">الاسم الكامل للأم <span class="text-red-500">*</span></label>
              <input v-model="form.mother_full_name" type="text" required class="mt-1 block w-full border rounded-md p-2 shadow-sm">
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">الجنس <span class="text-red-500">*</span></label>
                <select v-model="form.gender" required class="mt-1 block w-full border rounded-md p-2 shadow-sm bg-white">
                  <option value="male">ذكر</option>
                  <option value="female">أنثى</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">تاريخ الميلاد <span class="text-red-500">*</span></label>
                <input 
                    v-model="form.date_of_birth" 
                    type="date" 
                    required 
                    @keydown.prevent
                    class="mt-1 block w-full border rounded-md p-2 shadow-sm"
                >
              </div>
            </div>
          </div>
        </section>

        <!-- 2. Contact & School -->
        <section class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 class="text-lg font-bold text-gray-900 mb-4 pb-2 border-b">معلومات الاتصال والدراسة</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">رقم الهاتف <span class="text-red-500">*</span></label>
              <input 
                v-model="form.phone_number" 
                type="tel" 
                required 
                maxlength="11"
                placeholder="07XXXXXXXXX"
                class="mt-1 block w-full border rounded-md p-2 shadow-sm font-mono"
              >
              <p v-if="form.phone_number && form.phone_number.length !== 11" class="text-xs text-red-500 mt-1 font-bold">
                يجب أن يتكون رقم الهاتف من 11 رقمًا
              </p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">البريد الإلكتروني <span class="text-red-500">*</span></label>
              <input v-model="form.email_address" type="email" required class="mt-1 block w-full border rounded-md p-2 shadow-sm">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">رقم الامتحان <span class="text-red-500">*</span></label>
              <input v-model="form.examination_id" type="text" required class="mt-1 block w-full border rounded-md p-2 shadow-sm font-mono">
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">الفرع <span class="text-red-500">*</span></label>
                <select v-model="form.branch" required class="mt-1 block w-full border rounded-md p-2 shadow-sm bg-white">
                  <option value="scientific">علمي</option>
                  <option value="biology">أحيائي</option>
                  <option value="applied">تطبيقي</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">سنة التخرج <span class="text-red-500">*</span></label>
                <select v-model="graduation_year" required class="mt-1 block w-full border rounded-md p-2 shadow-sm bg-white">
                    <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
                </select>
              </div>
            </div>
          </div>
        </section>

        <!-- 3. Academic Data -->
        <section class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 class="text-lg font-bold text-gray-900 mb-4 pb-2 border-b">البيانات الأكاديمية</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">المعدل (%) <span class="text-red-500">*</span></label>
              <input 
                v-model="form.average" 
                type="number" 
                step="0.01" 
                min="50" 
                max="100" 
                required 
                class="mt-1 block w-full border rounded-md p-2 shadow-sm"
              >
              <p class="text-[10px] text-gray-500 mt-1">يجب أن يكون بين 50 و 100</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">المجموع الكلي <span class="text-red-500">*</span></label>
              <input v-model="form.total_sum" type="number" step="0.01" required class="mt-1 block w-full border rounded-md p-2 shadow-sm">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">عدد الدروس <span class="text-red-500">*</span></label>
              <input v-model="form.number_of_lessons" type="number" min="1" required class="mt-1 block w-full border rounded-md p-2 shadow-sm">
            </div>
          </div>
          <div class="mt-4">
            <label class="block text-sm font-medium text-gray-700">رفع الوثائق (PDF أو صور) <span class="text-red-500">*</span></label>
            <input @change="handleFileUpload" type="file" required class="mt-1 block w-full text-sm text-gray-500 file:ml-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100">
          </div>
        </section>

        <!-- 4. Department Preferences -->
        <section class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 class="text-lg font-bold text-gray-900 mb-4 pb-2 border-b">رغبات الأقسام</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">الرغبة الأولى <span class="text-red-500">*</span></label>
              <select v-model="form.department_preference_1" required class="mt-1 block w-full border rounded-md p-2 shadow-sm bg-white">
                <option v-for="dept in departments" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">الرغبة الثانية <span class="text-red-500">*</span></label>
              <select v-model="form.department_preference_2" required class="mt-1 block w-full border rounded-md p-2 shadow-sm bg-white">
                <option value="">لا يوجد</option>
                <option v-for="dept in availableDepts2" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">الرغبة الثالثة <span class="text-red-500">*</span></label>
              <select v-model="form.department_preference_3" required class="mt-1 block w-full border rounded-md p-2 shadow-sm bg-white">
                <option value="">لا يوجد</option>
                <option v-for="dept in availableDepts3" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
              </select>
            </div>
          </div>
        </section>

        <div v-if="error" class="bg-red-50 border-r-4 border-red-400 p-4">
          <p class="text-sm text-red-700 font-bold">{{ error }}</p>
        </div>

        <button 
          type="submit" 
          :disabled="submitting"
          class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-lg font-bold text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {{ submitting ? 'جاري إرسال الطلب...' : 'إرسال الاستمارة النهائية' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const auth = useAuthStore();

const loadingInitial = ref(true);
const submitting = ref(false);
const error = ref('');

const departments = ref([]);
const currentRound = ref(null);

const graduation_year = ref(new Date().getFullYear());
const years = computed(() => {
    const currentYear = new Date().getFullYear();
    const range = [];
    for (let i = currentYear; i >= 2000; i--) {
        range.push(i);
    }
    return range;
});

const form = ref({
  first_name: '',
  second_name: '',
  third_name: '',
  fourth_name: '',
  mother_full_name: '',
  gender: 'male',
  date_of_birth: '',
  phone_number: '',
  email_address: '',
  examination_id: '',
  branch: 'scientific',
  graduation_date: '',
  average: null,
  total_sum: null,
  number_of_lessons: null,
  department_preference_1: '',
  department_preference_2: '',
  department_preference_3: '',
});

const upload_document = ref(null);

const availableDepts2 = computed(() => {
  return departments.value.filter(d => d.id !== form.value.department_preference_1);
});

const availableDepts3 = computed(() => {
  return departments.value.filter(d => 
    d.id !== form.value.department_preference_1 && 
    d.id !== form.value.department_preference_2
  );
});

onMounted(async () => {
  if (!auth.voucherCode) return;
  
  try {
    const response = await api.get('initial-data/');
    departments.value = response.data.departments;
    currentRound.value = response.data.current_round;
    
    if (departments.value.length > 0) {
      form.value.department_preference_1 = departments.value[0].id;
    }
  } catch (err) {
    error.value = 'فشل في تحميل البيانات الأولية';
  } finally {
    loadingInitial.value = false;
  }
});

const handleFileUpload = (event) => {
  upload_document.value = event.target.files[0];
};

const submitApplication = async () => {
  if (form.value.phone_number.length !== 11) {
    error.value = 'يرجى إدخال رقم هاتف صحيح مكون من 11 رقمًا';
    return;
  }

  submitting.value = true;
  error.value = '';

  // Set graduation date to first day of selected year for backend compatibility
  form.value.graduation_date = `${graduation_year.value}-01-01`;

  const formData = new FormData();
  formData.append('voucher_code', auth.voucherCode);
  
  for (const key in form.value) {
    if (form.value[key] !== null && form.value[key] !== '') {
      formData.append(key, form.value[key]);
    }
  }
  
  if (upload_document.value) {
    formData.append('upload_document', upload_document.value);
  }

  try {
    await api.post('submit-application/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    auth.clearVoucher();
    router.push('/success');
  } catch (err) {
    const data = err.response?.data;
    if (data && typeof data === 'object') {
        error.value = 'يرجى التأكد من صحة البيانات المدخلة';
    } else {
      error.value = data?.error || 'فشل في إرسال الطلب. يرجى المحاولة لاحقاً';
    }
  } finally {
    submitting.value = false;
  }
};
</script>
