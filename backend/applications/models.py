from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
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

    BRANCH_CHOICES = [
        ('scientific', 'Scientific'),
        ('biology', 'Biology'),
        ('applied', 'Applied'),
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
    date_of_birth = models.DateField()

    examination_id = models.CharField(max_length=50, unique=True)
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES)
    graduation_date = models.DateField()

    # -----------------------------
    # Academic data
    # -----------------------------
    average = models.DecimalField(max_digits=5, decimal_places=2, db_index=True)
    total_sum = models.DecimalField(max_digits=8, decimal_places=2)
    number_of_lessons = models.PositiveIntegerField()

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
        if self.number_of_lessons <= 0:
            raise ValidationError("Number of lessons must be greater than zero.")

        # ✅ Date checks
        if self.date_of_birth >= date.today():
            raise ValidationError("Date of birth must be in the past.")

        if self.graduation_date > date.today():
            raise ValidationError("Graduation date cannot be in the future.")

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