from django.shortcuts import render, redirect
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponse
from openpyxl import Workbook
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Voucher, Application, Department, AdmissionRound
from .serializers import (
    VoucherSerializer, ApplicationSerializer, 
    DepartmentSerializer, AdmissionRoundSerializer
)

# =========================================================
# ✅ 1. Voucher Verification API
# =========================================================
@api_view(['POST'])
def verify_voucher(request):
    code = request.data.get('code', '').strip()
    if not code:
        return Response({'error': 'Please enter a voucher code'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        voucher = Voucher.objects.get(code=code)
        if voucher.is_used:
            return Response({'error': 'This voucher is already used'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = VoucherSerializer(voucher)
        return Response(serializer.data)

    except Voucher.DoesNotExist:
        return Response({'error': 'Invalid voucher code'}, status=status.HTTP_404_NOT_FOUND)

# =========================================================
# ✅ 2. Department & Round Info API
# =========================================================
@api_view(['GET'])
def initial_data(request):
    departments = Department.objects.filter(is_active=True)
    current_round = AdmissionRound.objects.filter(is_active=True).first()
    
    return Response({
        'departments': DepartmentSerializer(departments, many=True).data,
        'current_round': AdmissionRoundSerializer(current_round).data if current_round else None
    })

# =========================================================
# ✅ 3. Application Submission API
# =========================================================
class ApplicationCreateView(APIView):
    def post(self, request):
        voucher_code = request.data.get('voucher_code')
        try:
            voucher = Voucher.objects.get(code=voucher_code, is_used=False)
        except Voucher.DoesNotExist:
            return Response({'error': 'Invalid or used voucher'}, status=status.HTTP_400_BAD_REQUEST)

        current_round = AdmissionRound.objects.filter(is_active=True).first()
        if not current_round or not current_round.is_open():
            return Response({'error': 'Admission round is closed or not available'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            # Manual save to handle voucher association and status
            try:
                application = serializer.save(
                    voucher=voucher,
                    round=current_round,
                    status='submitted'
                )
                voucher.is_used = True
                voucher.save()
                return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# =========================================================
# ✅ 4. Check Status API
# =========================================================
@api_view(['GET'])
def check_status_api(request):
    code = request.query_params.get('code', '').strip()
    if not code:
        return Response({"error": "Voucher code is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        voucher = Voucher.objects.get(code=code)
        application = Application.objects.get(voucher=voucher)
        return Response(ApplicationSerializer(application).data)
    except (Voucher.DoesNotExist, Application.DoesNotExist):
        return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)

# =========================================================
# ✅ 5. Dashboard Stats API
# =========================================================
@api_view(['GET'])
def dashboard_stats(request):
    current_round = AdmissionRound.objects.filter(is_active=True).first()
    if not current_round:
        return Response({'error': 'No active round'}, status=status.HTTP_404_NOT_FOUND)

    applications = Application.objects.filter(round=current_round)
    
    stats = {
        'total_applications': applications.count(),
        'accepted': applications.filter(status='accepted').count(),
        'rejected': applications.filter(status='rejected').count(),
        'not_allocated': applications.filter(status='not_allocated').count(),
        'round': AdmissionRoundSerializer(current_round).data
    }

    departments = Department.objects.filter(is_active=True)
    dept_stats = []
    for dept in departments:
        assigned_count = applications.filter(assigned_department=dept).count()
        dept_stats.append({
            'name': dept.name,
            'capacity': dept.capacity,
            'assigned': assigned_count,
            'remaining': dept.capacity - assigned_count
        })
    stats['department_stats'] = dept_stats
    
    return Response(stats)

# =========================================================
# ✅ 6. Export Excel (Keep as is, but can be triggered via API)
# =========================================================
def export_applications_excel(request):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Applications"

    headers = ["Full Name", "Average", "Branch", "1st Preference", "2nd Preference", "3rd Preference", "Assigned Department", "Status", "Voucher Code"]
    sheet.append(headers)

    applications = Application.objects.select_related('department_preference_1', 'department_preference_2', 'department_preference_3', 'assigned_department', 'voucher').all()

    for app in applications:
        sheet.append([
            app.full_name, app.average, app.branch,
            app.department_preference_1.name if app.department_preference_1 else "",
            app.department_preference_2.name if app.department_preference_2 else "",
            app.department_preference_3.name if app.department_preference_3 else "",
            app.assigned_department.name if app.assigned_department else "",
            app.status, app.voucher.code
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=applications.xlsx'
    workbook.save(response)
    return response
