from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from decimal import Decimal
import secrets
import os

def validate_file_extension_and_size(value):
    # ✅ 1. Check Extension
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('نوع الملف غير مدعوم. يرجى رفع ملفات بصيغة PDF أو JPG أو PNG فقط.')
    
    # ✅ 2. Check Size (5MB Limit)
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('حجم الملف كبير جداً. يجب ألا يتجاوز حجم الملف 5 ميجابايت.')

# =========================================================
# ✅ Voucher Model
# =========================================================
class Voucher(models.Model):
    code = models.CharField(max_length=20, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_code(self):
        return "ENG-" + secrets.token_hex(4).upper()

    def save(self, *args, **kwargs):
        if not self.code:
            new_code = self.generate_code()

            while Voucher.objects.filter(code=new_code).exists():
                new_code = self.generate_code()

            self.code = new_code

        super().save(*args, **kwargs)

    def __str__(self):
        return self.code


# =========================================================
# ✅ Department Model
# =========================================================
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.capacity})"


# =========================================================
# ✅ Admission Round Model
# =========================================================
class AdmissionRound(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
 # ✅ NEW FIELD
    is_allocated = models.BooleanField(default=False)


    def is_open(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date.")

    def __str__(self):
        return self.name


# =========================================================
# ✅ Application Model
# =========================================================
class Application(models.Model):

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    FACULTY_CHILD_CHOICES = [
        ('yes', 'نعم'),
        ('no', 'كلا'),
    ]

    ADDED_LANGUAGE_CHOICES = [
        ('none', 'لا يوجد'),
        ('french', 'اللغة الفرنسية'),
        ('turkish', 'اللغة التركية'),
    ]

    # Choices for graduation attempt ("دور التخرج")
    GRADUATION_ATTEMPT_CHOICES = [
        ('first_round', 'الدور الأول'),
        ('second_round', 'الدور الثاني'),
        ('third_round', 'الدور الثالث'),
    ]

    BRANCH_CHOICES = [
        ('scientific', 'Scientific'),
        ('biology', 'Biology'),
        ('applied', 'Applied'),
    ]

    LESSON_COUNT_CHOICES = [
        (5, '5 دروس'),
        (6, '6 دروس'),
        (7, '7 دروس'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('not_allocated', 'Not Allocated'),
    ]

    voucher = models.OneToOneField(Voucher, on_delete=models.CASCADE)

    # -----------------------------
    # Student identity
    # -----------------------------
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    third_name = models.CharField(max_length=100)
    fourth_name = models.CharField(max_length=100)

    mother_full_name = models.CharField(max_length=255)

    # -----------------------------
    # Contact
    # -----------------------------
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField()

    # -----------------------------
    # Personal / school info
    # -----------------------------
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    is_faculty_child = models.CharField(
        max_length=5,
        choices=FACULTY_CHILD_CHOICES,
        default='no',
        verbose_name='هل انت من ابناء التدريسين'
    )
    date_of_birth = models.DateField()

    examination_id = models.CharField(max_length=50, unique=True)
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES)
    # Graduation attempt ("دور التخرج")
    graduation_attempt = models.CharField(
        max_length=20,
        choices=GRADUATION_ATTEMPT_CHOICES,
        default='first_round',
        verbose_name='دور التخرج'
    )
    graduation_date = models.CharField(
        max_length=9,
        verbose_name='سنة التخرج'
    )

    # Added language option ("اللغات المضافة")
    added_language = models.CharField(
        max_length=10,
        choices=ADDED_LANGUAGE_CHOICES,
        default='none',
        verbose_name='اللغات المضافة'
    )
    added_language_degree = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='درجة اللغة المضافة'
    )

    # -----------------------------
    # Academic data
    # -----------------------------
    average = models.DecimalField(max_digits=6, decimal_places=3, db_index=True)
    # Original total sum entered by student before additions
    original_total_sum = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name='المجموع الأصلي (قبل الإضافة)'
    )
    # Final total sum after bonus additions
    total_sum = models.DecimalField(max_digits=8, decimal_places=3, verbose_name='المجموع الكلي النهائي (بعد الإضافة)')
    number_of_lessons = models.PositiveIntegerField(
        choices=LESSON_COUNT_CHOICES,
        verbose_name='عدد الدروس'
    )

    # -----------------------------
    # Documents
    # -----------------------------
    upload_document = models.FileField(
        upload_to='documents/applications/',
        validators=[validate_file_extension_and_size],
        null=True,
        blank=True
    )

    # -----------------------------
    # Admission round
    # -----------------------------
    round = models.ForeignKey(
        'AdmissionRound',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications'
    )

    # -----------------------------
    # Preferences
    # -----------------------------
    department_preference_1 = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='first_choice_applications'
    )

    department_preference_2 = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='second_choice_applications'
    )

    department_preference_3 = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='third_choice_applications'
    )

    # -----------------------------
    # Allocation result
    # -----------------------------
    assigned_department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_students'
    )

    allocation_round = models.PositiveSmallIntegerField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='submitted'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # -----------------------------
    # ✅ VALIDATIONS
    # -----------------------------
    def clean(self):
        # ✅ Preferences must be unique
        preferences = [
            self.department_preference_1,
            self.department_preference_2,
            self.department_preference_3,
        ]

        selected = [p for p in preferences if p is not None]

        if len(selected) != len(set(selected)):
            raise ValidationError("Department preferences must be different.")

        # ✅ Average range
        if self.average < 0 or self.average > 100:
            raise ValidationError("Average must be between 0 and 100.")

        # ✅ Lessons
        if self.number_of_lessons not in [5, 6, 7]:
            raise ValidationError("عدد الدروس غير مسموح به. يجب اختيار 5، 6، أو 7 دروس فقط.")

        # ✅ Date checks
        if self.date_of_birth >= date.today():
            raise ValidationError("Date of birth must be in the past.")

        # graduation_date is stored as an academic year string (e.g. "2025-2026"), no date comparison needed

        # ✅ Added language validation
        if self.added_language in ['french', 'turkish']:
            if self.added_language_degree is None:
                raise ValidationError("يرجى إدخال درجة اللغة المضافة.")
            if self.added_language_degree < 0 or self.added_language_degree > 100:
                raise ValidationError("درجة اللغة المضافة يجب أن تكون بين 0 و 100.")

    def save(self, *args, **kwargs):
        # ✅ Automatically add all bonus marks (Graduation, Language, Faculty Child) on new application creation
        if not self.pk:
            # Preserve the exact sum entered by the student before additions
            if self.original_total_sum is None and self.total_sum is not None:
                self.original_total_sum = Decimal(str(self.total_sum))

            bonus = Decimal('0.00')

            # 1. Graduation Attempt Bonus (+7 for First Round)
            if self.graduation_attempt == 'first_round':
                bonus += Decimal('7.00')

            # 2. Added Language Bonus (french or turkish degree * 0.08)
            if self.added_language in ['french', 'turkish'] and self.added_language_degree is not None:
                language_bonus = Decimal(str(self.added_language_degree)) * Decimal('0.08')
                bonus += language_bonus
            else:
                self.added_language_degree = None

            # 3. Faculty Child Bonus (5 * number_of_lessons)
            if self.is_faculty_child == 'yes' and self.number_of_lessons and self.number_of_lessons > 0:
                faculty_bonus = Decimal('5.00') * Decimal(str(self.number_of_lessons))
                bonus += faculty_bonus

            # Calculate final total sum = original_total_sum + all bonuses
            if self.original_total_sum is not None:
                self.total_sum = Decimal(str(self.original_total_sum)) + bonus
            
            # Recalculate average based on updated total_sum and number_of_lessons
            if self.number_of_lessons and self.number_of_lessons > 0:
                self.average = round(Decimal(str(self.total_sum)) / Decimal(str(self.number_of_lessons)), 2)

        super().save(*args, **kwargs)

    # -----------------------------
    # Display helpers
    # -----------------------------
    @property
    def full_name(self):
        return f"{self.first_name} {self.second_name} {self.third_name} {self.fourth_name}"

    def __str__(self):
        return f"{self.full_name} - {self.voucher.code}"

    class Meta:
        ordering = ['-average', 'created_at']