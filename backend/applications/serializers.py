from rest_framework import serializers
from .models import Voucher, Department, AdmissionRound, Application

# =========================================================
# ✅ Voucher Serializer
# =========================================================
class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = ['id', 'code', 'is_used', 'created_at']
        read_only_fields = ['id', 'code', 'is_used', 'created_at']

# =========================================================
# ✅ Department Serializer
# =========================================================
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'capacity', 'is_active']

# =========================================================
# ✅ Admission Round Serializer
# =========================================================
class AdmissionRoundSerializer(serializers.ModelSerializer):
    is_open = serializers.ReadOnlyField()

    class Meta:
        model = AdmissionRound
        fields = ['id', 'name', 'start_date', 'end_date', 'is_active', 'is_allocated', 'is_open']

# =========================================================
# ✅ Application Serializer
# =========================================================
class ApplicationSerializer(serializers.ModelSerializer):
    voucher_code = serializers.CharField(source='voucher.code', read_only=True)
    full_name = serializers.ReadOnlyField()
    
    # Nested display for related fields
    round_name = serializers.CharField(source='round.name', read_only=True)
    pref_1_name = serializers.CharField(source='department_preference_1.name', read_only=True)
    pref_2_name = serializers.CharField(source='department_preference_2.name', read_only=True)
    pref_3_name = serializers.CharField(source='department_preference_3.name', read_only=True)
    assigned_dept_name = serializers.CharField(source='assigned_department.name', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'voucher', 'voucher_code', 'first_name', 'second_name', 'third_name', 'fourth_name',
            'full_name', 'mother_full_name', 'phone_number', 'email_address', 'gender', 'date_of_birth',
            'examination_id', 'branch', 'graduation_date', 'average', 'total_sum', 'number_of_lessons',
            'upload_document', 'round', 'round_name', 'department_preference_1', 'pref_1_name',
            'department_preference_2', 'pref_2_name', 'department_preference_3', 'pref_3_name',
            'assigned_department', 'assigned_dept_name', 'allocation_round', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'voucher', 'assigned_department', 'allocation_round', 'status', 'created_at']

    def validate(self, data):
        # Add any cross-field validation here if needed beyond model's clean()
        # Note: DRF calls validate(), but model's clean() isn't called automatically on save().
        return data
