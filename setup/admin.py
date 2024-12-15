# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Company
from .models import Department

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'logo_preview',
        'name', 
        'registration_number',
        'email',
        'phone',
        'is_active',
        'created_by',
        'created_at'
    ]
    
    list_filter = [
        'is_active',
        'country',
        'state',
        'created_at',
        ('created_by', admin.RelatedOnlyFieldListFilter),
    ]
    
    search_fields = [
        'name',
        'trading_name',
        'registration_number',
        'tax_number',
        'email',
        'phone',
        'address_line1',
        'city',
    ]
    
    readonly_fields = [
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        'logo_preview_large'
    ]
    
    fieldsets = [
        (_('Basic Information'), {
            'fields': (
                'name',
                'trading_name',
                'description',
                ('logo', 'logo_preview_large'),
            )
        }),
        (_('Registration Details'), {
            'fields': (
                'registration_number',
                'tax_number',
                'establishment_date',
            )
        }),
        (_('Contact Information'), {
            'fields': (
                'email',
                'phone',
                'website',
            )
        }),
        (_('Address'), {
            'fields': (
                'address_line1',
                'address_line2',
                ('city', 'state'),
                ('country', 'postal_code'),
            )
        }),
        (_('Status'), {
            'fields': (
                'is_active',
            )
        }),
        (_('System Information'), {
            'classes': ('collapse',),
            'fields': (
                ('created_by', 'created_at'),
                ('updated_by', 'updated_at'),
            )
        }),
    ]
    
    list_per_page = 25
    date_hierarchy = 'created_at'
    list_display_links = ['name']
    list_editable = ['is_active']
    save_on_top = True
    
    def logo_preview(self, obj):
        """Small logo preview for list display"""
        if obj.logo:
            return format_html(
                '<img src="{}" style="width: 30px; height: 30px; object-fit: contain;"/>',
                obj.logo.url
            )
        return "-"
    logo_preview.short_description = _('Logo')
    
    def logo_preview_large(self, obj):
        """Larger logo preview for detail view"""
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px;"/>',
                obj.logo.url
            )
        return _("No logo uploaded")
    logo_preview_large.short_description = _('Logo Preview')
    
    def save_model(self, request, obj, form, change):
        """Auto-set the user when saving the model"""
        if not change:  # If creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """Optimize queries by prefetching related fields"""
        return super().get_queryset(request).select_related(
            'created_by',
            'updated_by'
        )
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import LocationType, CompanyLocation, LocationAuditLog

@admin.register(LocationType)
class LocationTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_internal', 'is_active', 'created_by', 'created_at']
    list_filter = ['is_internal', 'is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class LocationAuditLogInline(admin.TabularInline):
    model = LocationAuditLog
    readonly_fields = ['action', 'field_name', 'old_value', 'new_value', 'timestamp', 'user', 'ip_address']
    extra = 0
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(CompanyLocation)
class CompanyLocationAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'company',
        'location_type',
        'status',
        'is_headquarters',
        'city',
        'country',
        'contact_person',
    ]
    
    list_filter = [
        'status',
        'location_type',
        'is_headquarters',
        'country',
        'created_at',
    ]
    
    search_fields = [
        'name',
        'code',
        'company__name',
        'contact_person',
        'contact_email',
        'address_line1',
        'city',
    ]
    
    readonly_fields = [
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
    ]
    
    fieldsets = [
        (_('Basic Information'), {
            'fields': (
                'company',
                'location_type',
                'name',
                'code',
                'status',
                'is_headquarters',
            )
        }),
        (_('Contact Information'), {
            'fields': (
                'contact_person',
                'contact_email',
                'contact_phone',
            )
        }),
        (_('Address'), {
            'fields': (
                'address_line1',
                'address_line2',
                ('city', 'state'),
                ('country', 'postal_code'),
                ('latitude', 'longitude'),
            )
        }),
        (_('Additional Information'), {
            'fields': (
                'operating_hours',
                'notes',
            )
        }),
        (_('Audit Information'), {
            'classes': ('collapse',),
            'fields': (
                ('created_by', 'created_at'),
                ('updated_by', 'updated_at'),
            )
        }),
    ]
    
    inlines = [LocationAuditLogInline]
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
        
        # Create audit log
        if change:
            changed_fields = form.changed_data
            for field_name in changed_fields:
                LocationAuditLog.objects.create(
                    location=obj,
                    action='update',
                    field_name=field_name,
                    old_value=str(form.initial.get(field_name, '')),
                    new_value=str(getattr(obj, field_name)),
                    user=request.user,
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
        else:
            LocationAuditLog.objects.create(
                location=obj,
                action='create',
                user=request.user,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

    def delete_model(self, request, obj):
        LocationAuditLog.objects.create(
            location=obj,
            action='delete',
            user=request.user,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        super().delete_model(request, obj)

@admin.register(LocationAuditLog)
class LocationAuditLogAdmin(admin.ModelAdmin):
    list_display = ['location', 'action', 'field_name', 'user', 'timestamp']
    list_filter = ['action', 'timestamp', 'user']
    search_fields = ['location__name', 'field_name', 'user__username']
    readonly_fields = ['location', 'action', 'field_name', 'old_value', 'new_value', 
                      'timestamp', 'user', 'ip_address', 'user_agent']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['Code','name', 'company', 'is_main_department', 'is_ipd', 'is_laboratory', 'is_active']
    list_filter = ['is_main_department', 'is_ipd', 'is_active', 'is_laboratory', 'company']
    search_fields = ['name', 'responsible_person', 'income_account', 'expense_account']
    readonly_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']
    fieldsets = [
        ('Basic Information', {
            'fields': ('Code','name', 'company', 'locations', 'responsible_person', 'is_main_department')
        }),
        ('Department Options', {
            'fields': ('is_ipd', 'ipd_value_percentage', 'is_medical_package', 'issue_inventory')
        }),
        ('Laboratory and Operation Theater', {
            'fields': ('is_laboratory', 'laboratory_type', 'outside_value_percentage','is_operation_theater', 'operation_theater_date_mandatory')
        }),
        ('Discount and Accounts', {
            'fields': ('allow_discounts', 'max_discount_percentage', 'income_account', 'expense_account')
        }),
        ('Invoice and Sequence Options', {
            'fields': ('modify_invoice_number', 'issue_sequence_number', 'issue_sequence_auto',
                       'department_wise_sequence', 'department_sequence_per_day')
        }),
        ('Status and Audit', {
            'fields': ('is_active', 'created_by', 'created_at', 'updated_by', 'updated_at')
        }),
    ]
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


from .models import ClassDetail

@admin.register(ClassDetail)
class ClassDetailAdmin(admin.ModelAdmin):
    list_display = ['class_code', 'name', 'accounting_enabled', 'is_active']
    list_filter = ['accounting_enabled', 'is_active']
    search_fields = ['class_code', 'name', 'management_account_id']
    readonly_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']
    fieldsets = [
        ('Basic Information', {
            'fields': ('class_code', 'name', 'description')
        }),
        ('Management Account & Accounting', {
            'fields': ('management_account_id', 'accounting_enabled', 'income_account', 'expense_account', 'max_posting_limit')
        }),
        ('Relationships', {
            'fields': ('departments',)
        }),
        ('Status and Audit', {
            'fields': ('is_active', 'created_by', 'created_at', 'updated_by', 'updated_at')
        }),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


 
from .models import ClarificationDetail

@admin.register(ClarificationDetail)
class ClarificationDetailAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_income', 'is_expense', 'is_active', 'requires_approval']
    list_filter = ['is_income', 'is_expense', 'is_adjustment', 'requires_approval', 'is_active']
    search_fields = ['code', 'name', 'description']
    readonly_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']
    fieldsets = [
        ('Basic Information', {
            'fields': ('code', 'name', 'description')
        }),
        ('Transaction Segregation', {
            'fields': ('is_income', 'is_expense', 'is_adjustment')
        }),
        ('Advanced Options', {
            'fields': ('requires_approval', 'auto_post', 'max_transaction_value')
        }),
        ('Relationships', {
            'fields': ('departments',)
        }),
        ('Audit and Status', {
            'fields': ('is_active', 'created_by', 'created_at', 'updated_by', 'updated_at')
        }),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

from .models import  UserCompany, UserLocation

@admin.register(UserCompany)
class UserCompanyAdmin(admin.ModelAdmin):
    list_display = ['user', 'company']
    search_fields = ['user__username', 'company__name']
    list_filter = ['company']

@admin.register(UserLocation)
class UserLocationAdmin(admin.ModelAdmin):
    list_display = ['user', 'company','location']
    search_fields = ['user__username', 'location__name']
    list_filter = ['company','location']

from .models import LaboratoryDepartment

@admin.register(LaboratoryDepartment)
class LaboratoryDepartmentAdmin(admin.ModelAdmin):
    list_display = ['Code','name', 'company', 'is_main_department', 'is_active']
    list_filter = ['is_main_department',  'is_active', 'company']
    search_fields = ['name', 'responsible_person', ]
    readonly_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']
    fieldsets = [
        ('Basic Information', {
            'fields': ('Code','name', 'company', 'locations', 'responsible_person', 'is_main_department')
        }),
        ('Status and Audit', {
            'fields': ('is_active', 'created_by', 'created_at', 'updated_by', 'updated_at')
        }),
    ]
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

from .models import TaxCode

@admin.register(TaxCode)
class TaxCodeAdmin(admin.ModelAdmin):
    list_display = ['code','rate','name', 'sequence','company',  'is_active',]
    list_filter = ['name',  'is_active', 'company']
    search_fields = ['name', 'rate', ]
    readonly_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']
    fieldsets = [
        ('Basic Information', {
            'fields': ('code','rate','name', 'sequence' ,'company', 'locations')
        }),
        ('Status and Audit', {
            'fields': ('is_active', 'created_by', 'created_at', 'updated_by', 'updated_at')
        }),
    ]
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['service_code','service_name','rate', 'cost_price','minimum_price','departments','company',  'is_active',]
    list_filter = ['service_code','service_name',  'is_active','departments', 'company']
    search_fields = ['service_name','service_code', 'departments', ]
    readonly_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']
    fieldsets = [
        ('Related Information', {
            'fields': ('departments','company', 'locations')
        }),
        ('Basic Information', {
            'fields': ('service_code','service_name','rate', 'cost_price' ,'minimum_price','rate_per_day', 'item_barcode','remarks')
        }),
         ('Laboratory Information', {
            'fields': ('laboratory_departments','print_lab_note')
        }),
         ('Other Information', {
            'fields': ('highlight_in_diagnosis_sheet','allowed_discount','max_allowed_discount')
        }),
        ('Tax Information', {
            'fields': ('tax_code','include_tax')
        }),
        ('Status and Audit', {
            'fields': ('is_active', 'created_by', 'created_at', 'updated_by', 'updated_at')
        }),
    ]
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

 
from .models import ServiceTax

@admin.register(ServiceTax)
class ServiceTaxAdmin(admin.ModelAdmin):
    list_display = ['service_code', 'company', 'is_active', 'include_tax']
    list_filter = ['company', 'is_active', 'include_tax']
    search_fields = ['service_code__name', 'company__name']  # Adjust based on field names
    readonly_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']
    filter_horizontal = ['locations', 'tax_code']  # For ManyToMany fields
    fieldsets = [
        ('Related Information', {
            'fields': ('company', 'locations', 'service_code')
        }),
        ('Tax Information', {
            'fields': ('tax_code', 'include_tax', 'remarks')
        }),
        ('Status and Audit', {
            'fields': ('is_active', 'created_by', 'created_at', 'updated_by', 'updated_at')
        }),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)



from .models import ServiceLocationPrice


@admin.register(ServiceLocationPrice)
class ServiceLocationPriceAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ['locations','service_code', 'rate', 'cost_price', 'minimum_price', 'company', 'is_active']
    list_filter = ['service_code', 'is_active', 'company']
    search_fields = ['service_code__service_name', 'company__name']  # Adjusted for more effective search
    readonly_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']

    # Fieldsets for organized editing
    fieldsets = [
        ('Related Information', {
            'fields': ('company', 'locations'),
        }),
        ('Basic Information', {
            'fields': ('service_code', 'rate', 'cost_price', 'minimum_price', 'rate_per_day', 'item_barcode', 'remarks'),
        }),
        ('Laboratory Information', {
            'fields': ('print_lab_note',),
        }),
        ('Discount Information', {
            'fields': ('allowed_discount', 'max_allowed_discount'),
        }),
        ('Status and Audit', {
            'fields': ('is_active', 'created_by', 'created_at', 'updated_by', 'updated_at'),
        }),
    ]

    # Save model logic for tracking created_by and updated_by fields
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.created_by = request.user
        obj.updated_by = request.user  # Always update the updated_by field
        super().save_model(request, obj, form, change)

    # Optional: Customize queryset to prefetch related data for optimization
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('company', 'locations', 'service_code')

    # Optional: Improve the display of `service_code` in the list view
    def service_code(self, obj):
        return obj.service_code.service_name  # Adjust `service_name` to match your `Service` model
    service_code.admin_order_field = 'service_code'  # Enable ordering by service_code
    service_code.short_description = 'Service Code'




from .models import ConsultationSupplierType

@admin.register(ConsultationSupplierType)
class ConsultationSupplierTypeAdmin(admin.ModelAdmin):
    list_display = ['Code','Description','company', 'is_active',]
    list_filter = ['Code',  'Description', 'company']
    search_fields = ['Code', 'Description', ]
    readonly_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']
    fieldsets = [
        ('Basic Information', {
            'fields': ('company', 'locations','Code','Description','remarks',)
        }),
        ('Status and Audit', {
            'fields': ('is_active', 'created_by', 'created_at', 'updated_by', 'updated_at')
        }),
    ]
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

 
 
from .models import SupplierRegistration


@admin.register(SupplierRegistration)
class SupplierRegistrationAdmin(admin.ModelAdmin):
    list_display = [
        'sup_user_code', 'sup_name', 'company', 'sup_type_sys_code', 'is_active',
    ]
    list_filter = [
        'sup_type_sys_code', 'company', 'gender', 'is_active',
    ]
    search_fields = [
        'sup_user_code', 'sup_name', 'contact_person', 'email',
    ]
    readonly_fields = [
        'created_by', 'created_at', 'updated_by', 'updated_at',
    ]
    fieldsets = [
        ('Basic Information', {
            'fields': (
                'sup_user_code', 'sup_name', 'sup_type_sys_code', 'gender',
                'date_of_birth', 'company', 'locations', 'departments','con_user_code', 'contact_person',
            ),
        }),
        ('Contact Details', {
            'fields': (
                'add1', 'add2', 'add3', 'tel1', 'tel2', 'tele3', 'fax', 'email', 'web','remarks','sms_name',
            ),
        }),
        ('Tax and Financial Details', {
            'fields': ( 
                'app_wtax', 'app_wtax_pre',
                'app_wtax_no', 
                'full_acc_code', 'sub_acc_sys_code', 'vat_no', 'tqb_no',
                'boi_no', 'license_number', 'edb_no',
            ),
        }),
        ('Invoice Settings', {
            'fields': (
                'invoice_code', 'inv_no_sup_wise', 'dep_wise_sequence_no_yes', 'e_channeling_ref_no',
            ),
        }),
        ('Status and Audit', {
            'fields': (
                'is_active',  'created_by', 'created_at', 'updated_by', 'updated_at',
            ),
        }),
    ]

    # def company_display(self, obj):
    #     """
    #     Display related companies as a comma-separated string.
    #     """
    #     return ", ".join([company.name for company in obj.company.all()])

    # company_display.short_description = 'Company'

    def save_model(self, request, obj, form, change):
        if not change:  # If the object is being created for the first time
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)



 
 
 
from .models import SupplierDepartmentDetails


@admin.register(SupplierDepartmentDetails)
class SupplierDepartmentDetailsAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = (
        'company', 
        'locations', 
        'supplier', 
        'departments', 
        'services_code', 
        'hospital_services_code', 
        'channeling_rate', 
        'is_doctor_fees',
        'hospital_rate', 
        'rate_cost_per_day', 
        'number_of_appointments', 
        'appointment_duration', 
        'is_active',
        'created_at',
        'updated_at'
    )
    
    # Fields to filter the records in the admin view
    list_filter = (
        'company', 
        'locations', 
        'supplier', 
        'departments', 
        'is_active'
    )
    
    # Fields to search for in the admin view
    search_fields = (
        'company__name', 
        'locations__name', 
        'supplier__name', 
        'departments__name', 
        'services_code__name',
        'hospital_services_code__name',
    )
    
    # Readonly fields (for audit purposes)
    readonly_fields = ('created_by', 
                'updated_by', 'created_at', 'updated_at')
    
    # Fields to display in the admin form (layout control)
    fieldsets = (
        ('Company and Location Details', {
            'fields': ('company', 'locations')
        }),
        ('Supplier Information', {
            'fields': ('supplier',)
        }),
        ('Department and Service Information', {
            'fields': (
                'departments', 
                'services_code', 
                'hospital_services_code'
            )
        }),
        ('Rates and Fees', {
            'fields': (
                'channeling_rate', 
                'hospital_rate', 
                'rate_cost_per_day', 
                'is_doctor_fees'
            )
        }),
        ('Appointment Details', {
            'fields': (
                'number_of_appointments', 
                'appointment_duration'
            )
        }),
        ('Audit Fields', {
            'fields': (
                'is_active', 
                'created_by', 
                'updated_by', 
                'created_at', 
                'updated_at'
            )
        }),
    )
    
    # Enable saving the user who creates/updates the record
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)



from django.contrib import admin
from .models import SupplierReferralFeeDetails

@admin.register(SupplierReferralFeeDetails)
class SupplierReferralFeeDetailsAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'departments', 'services_code', 'ReferralFee', 'ReferralFeePre', 'is_active']
    list_filter = ['supplier', 'departments', 'is_active']
    search_fields = ['supplier__name', 'departments__name', 'services_code__name']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
