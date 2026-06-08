from django.urls import path
from . import views

urlpatterns = [
    # API Endpoints
    path('api/verify-voucher/', views.verify_voucher, name='api_verify_voucher'),
    path('api/initial-data/', views.initial_data, name='api_initial_data'),
    path('api/submit-application/', views.ApplicationCreateView.as_view(), name='api_submit_application'),
    path('api/check-status/', views.check_status_api, name='api_check_status'),
    path('api/dashboard-stats/', views.dashboard_stats, name='api_dashboard_stats'),
    
    # Utilities
    path('export-excel/', views.export_applications_excel, name='export_excel'),
]
