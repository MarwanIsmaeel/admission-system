from django.contrib import admin, messages
from django.db import transaction
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Voucher, Application, Department, AdmissionRound


# =========================================================
# ✅ Export Action
# =========================================================
@admin.action(description='Export selected applications to Excel')
def export_to_excel(modeladmin, request, queryset):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Applications"

    headers = [
        "Full Name", "Average", "Branch", "Exam ID", "1st Choice", "2nd Choice", "3rd Choice", 
        "Assigned Department", "Status", "Phone", "Email", "Voucher"
    ]
    sheet.append(headers)

    for app in queryset.select_related(
        'department_preference_1', 'department_preference_2', 'department_preference_3', 
        'assigned_department', 'voucher'
    ):
        sheet.append([
            app.full_name,
            app.average,
            app.branch,
            app.examination_id,
            app.department_preference_1.name if app.department_preference_1 else "",
            app.department_preference_2.name if app.department_preference_2 else "",
            app.department_preference_3.name if app.department_preference_3 else "",
            app.assigned_department.name if app.assigned_department else "",
            app.status,
            app.phone_number,
            app.email_address,
            app.voucher.code
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=applications_export.xlsx'
    workbook.save(response)
    return response


# =========================================================
# ✅ Voucher Admin
# =========================================================
@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ['code', 'is_used', 'created_at']
    readonly_fields = ['code']
    list_filter = ['is_used', 'created_at']
    search_fields = ['code']
    ordering = ['-created_at']


# =========================================================
# ✅ Department Admin
# =========================================================
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'is_active']
    search_fields = ['name']
    list_filter = ['is_active']


# =========================================================
# ✅ ✅ Allocation per ROUND ✅
# =========================================================
@admin.action(description='Run allocation for selected round')
def run_allocation_for_round(modeladmin, request, queryset):

    if queryset.count() != 1:
        modeladmin.message_user(
            request,
            "Please select exactly ONE round.",
            level=messages.ERROR
        )
        return

    selected_round = queryset.first()

    # ✅ Round must be closed
    if selected_round.is_active:
        modeladmin.message_user(
            request,
            "Round is still active. Please deactivate it first.",
            level=messages.ERROR
        )
        return

    # ✅ Prevent double allocation
    if selected_round.is_allocated:
        modeladmin.message_user(
            request,
            "This round is already allocated. Reset it first if needed.",
            level=messages.ERROR
        )
        return

    with transaction.atomic():

        departments = Department.objects.filter(is_active=True)

        if not departments.exists():
            modeladmin.message_user(
                request,
                "No active departments found.",
                level=messages.ERROR
            )
            return

        capacity_map = {d.id: d.capacity for d in departments}
        assigned_count = {d.id: 0 for d in departments}

        applications = Application.objects.filter(
            round=selected_round
        ).exclude(
            status__in=['draft', 'rejected']
        ).order_by('-average', 'created_at', 'id')

        if not applications.exists():
            modeladmin.message_user(
                request,
                "No applications found for this round.",
                level=messages.WARNING
            )
            return

        # ✅ Reset before allocation
        applications.update(
            assigned_department=None,
            allocation_round=None,
            status='submitted'
        )

        accepted = 0
        not_allocated = 0

        for app in applications:

            assigned = False

            preferences = [
                app.department_preference_1,
                app.department_preference_2,
                app.department_preference_3
            ]

            for i, dept in enumerate(preferences, start=1):

                if not dept:
                    continue

                if assigned_count[dept.id] < capacity_map[dept.id]:

                    app.assigned_department = dept
                    app.allocation_round = i
                    app.status = 'accepted'
                    app.save(update_fields=[
                        'assigned_department',
                        'allocation_round',
                        'status'
                    ])

                    assigned_count[dept.id] += 1
                    accepted += 1
                    assigned = True
                    break

            if not assigned:
                app.status = 'not_allocated'
                app.assigned_department = None
                app.allocation_round = None
                app.save(update_fields=[
                    'status',
                    'assigned_department',
                    'allocation_round'
                ])
                not_allocated += 1

        # ✅ MARK ROUND AS ALLOCATED
        selected_round.is_allocated = True
        selected_round.save(update_fields=['is_allocated'])

        modeladmin.message_user(
            request,
            f"✅ Allocation completed for '{selected_round.name}'. "
            f"Accepted: {accepted}, Not Allocated: {not_allocated}",
            level=messages.SUCCESS
        )


# =========================================================
# ✅ Reset allocation per round
# =========================================================
@admin.action(description='Reset allocation for selected round')
def reset_allocation_for_round(modeladmin, request, queryset):

    if queryset.count() != 1:
        modeladmin.message_user(request, "Select one round.", level=messages.ERROR)
        return

    selected_round = queryset.first()

    applications = Application.objects.filter(round=selected_round)

    count = applications.update(
        assigned_department=None,
        allocation_round=None,
        status='submitted'
    )

    # ✅ reset flag
    selected_round.is_allocated = False
    selected_round.save(update_fields=['is_allocated'])

    modeladmin.message_user(
        request,
        f"✅ Reset {count} applications for round '{selected_round.name}'",
        level=messages.SUCCESS
    )


# =========================================================
# ✅ Admission Round Admin
# =========================================================
@admin.register(AdmissionRound)
class AdmissionRoundAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'is_active', 'is_allocated']
    actions = [run_allocation_for_round, reset_allocation_for_round]


# =========================================================
# ✅ Application Admin
# =========================================================
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = [
        'full_name_display',
        'average',
        'round',
        'assigned_department',
        'allocation_round',
        'status',
        'created_at',
    ]

    list_filter = [
        'round',
        'status',
        'branch',
        'assigned_department',
        'created_at',
    ]

    search_fields = [
        'first_name',
        'second_name',
        'third_name',
        'fourth_name',
        'email_address',
        'voucher__code',
    ]

    ordering = ['-average', 'created_at']

    readonly_fields = ['voucher', 'created_at']

    actions = [export_to_excel]

    def full_name_display(self, obj):
        return obj.full_name