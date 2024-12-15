# models.py
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, EmailValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint

 


class TimeStampedUserModel(models.Model):
    """Abstract base class with created and modified timestamps and user tracking"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='%(class)s_created',
        verbose_name=_('Created by')
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='%(class)s_updated',
        verbose_name=_('Updated by')
    )

    class Meta:
        abstract = True

def validate_file_size(value):
    """Validate file size (limit to 5MB)"""
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB
        raise ValidationError("Maximum file size is 5MB")

class Company(TimeStampedUserModel):
    # Basic Information
    name = models.CharField(
        _('Company Name'),
        max_length=255,
        validators=[MinLengthValidator(2)],
        unique=True,
        help_text=_('Full registered name of the company')
    )
    trading_name = models.CharField(
        _('Trading Name'),
        max_length=255,
        blank=True,
        help_text=_('Business name used for trading (if different from registered name)')
    )
    
    # Registration Information
    registration_number = models.CharField(
        _('Registration Number'),
        max_length=50,
        unique=True,
        help_text=_('Official company registration number')
    )
    tax_number = models.CharField(
        _('Tax ID Number'),
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        help_text=_('Tax identification number')
    )
    
    # Contact Information
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(
        _('Phone Number'),
        validators=[phone_regex],
        max_length=17,
        help_text=_('Primary contact number')
    )
    email = models.EmailField(
        _('Email Address'),
        validators=[EmailValidator()],
        help_text=_('Primary contact email')
    )
    website = models.URLField(
        _('Website'),
        blank=True,
        help_text=_('Company website URL')
    )
    
    # Address Information
    address_line1 = models.CharField(
        _('Address Line 1'),
        max_length=255,
        help_text=_('Street address')
    )
    address_line2 = models.CharField(
        _('Address Line 2'),
        max_length=255,
        blank=True,
        help_text=_('Apartment, suite, unit, etc.')
    )
    city = models.CharField(
        _('City'),
        max_length=100,
        help_text=_('City name')
    )
    state = models.CharField(
        _('State/Province'),
        max_length=100,
        help_text=_('State or province name')
    )
    country = models.CharField(
        _('Country'),
        max_length=100,
        help_text=_('Country name')
    )
    postal_code = models.CharField(
        _('Postal Code'),
        max_length=20,
        help_text=_('Postal or ZIP code')
    )
    
    # Additional Information
    logo = models.ImageField(
        _('Company Logo'),
        upload_to='company_logos/',
        validators=[validate_file_size],
        blank=True,
        null=True,
        help_text=_('Company logo (max 5MB)')
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        help_text=_('Brief description of the company')
    )
    establishment_date = models.DateField(
        _('Establishment Date'),
        null=True,
        blank=True,
        help_text=_('Date when company was established')
    )
    
    # Status
    is_active = models.BooleanField(
        _('Active Status'),
        default=True,
        help_text=_('Whether the company is currently active')
    )
    
    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['registration_number']),
        ]
        permissions = [
            ("view_company_details", "Can view company details"),
            ("manage_company", "Can manage company information"),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        """Custom validation"""
        if self.establishment_date and self.establishment_date > timezone.now().date():
            raise ValidationError({
                'establishment_date': _('Establishment date cannot be in future')
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

 


class LocationType(models.Model):
    """Model to store different types of locations"""
    name = models.CharField(_('Type Name'), max_length=100, unique=True)
    is_internal = models.BooleanField(
        _('Is Internal'),
        default=True,
        help_text=_('Whether this is an internal or external location type')
    )
    description = models.TextField(_('Description'), blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='location_types_created'
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='location_types_updated'
    )

    class Meta:
        verbose_name = _('Location Type')
        verbose_name_plural = _('Location Types')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({'Internal' if self.is_internal else 'External'})"

class CompanyLocation(models.Model):
    """Model to store company location details"""
    
    # Location Status Choices
    class LocationStatus(models.TextChoices):
        ACTIVE = 'AC', _('Active')
        INACTIVE = 'IN', _('Inactive')
        TEMPORARY = 'TP', _('Temporary')
        UNDER_MAINTENANCE = 'UM', _('Under Maintenance')

    # Basic Information
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        related_name='locations',
        verbose_name=_('Company')
    )
    location_type = models.ForeignKey(
        LocationType,
        on_delete=models.PROTECT,
        related_name='locations',
        verbose_name=_('Location Type')
    )
    name = models.CharField(_('Location Name'), max_length=255)
    code = models.CharField(
        _('Location Code'),
        max_length=50,
        unique=True,
        help_text=_('Unique identifier for this location')
    )
    
    # Contact Information
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Phone number must be entered in format: '+999999999'. Up to 15 digits allowed.")
    )
    contact_person = models.CharField(_('Contact Person'), max_length=255)
    contact_email = models.EmailField(_('Contact Email'))
    contact_phone = models.CharField(
        _('Contact Phone'),
        validators=[phone_regex],
        max_length=17
    )
    
    # Address Information
    address_line1 = models.CharField(_('Address Line 1'), max_length=255)
    address_line2 = models.CharField(_('Address Line 2'), max_length=255, blank=True)
    city = models.CharField(_('City'), max_length=100)
    state = models.CharField(_('State/Province'), max_length=100)
    country = models.CharField(_('Country'), max_length=100)
    postal_code = models.CharField(_('Postal Code'), max_length=20)
    
    # GPS Coordinates
    latitude = models.DecimalField(
        _('Latitude'),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        _('Longitude'),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    
    # Operating Hours
    operating_hours = models.JSONField(
        _('Operating Hours'),
        null=True,
        blank=True,
        help_text=_('Store opening hours in JSON format')
    )
    
    # Status and Metadata
    status = models.CharField(
        _('Status'),
        max_length=2,
        choices=LocationStatus.choices,
        default=LocationStatus.ACTIVE
    )
    is_headquarters = models.BooleanField(
        _('Is Headquarters'),
        default=False
    )
    notes = models.TextField(_('Notes'), blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='locations_created'
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='locations_updated'
    )

    class Meta:
        verbose_name = _('Company Location')
        verbose_name_plural = _('Company Locations')
        ordering = ['company', 'name']
        unique_together = [['company', 'name']]
        indexes = [
            models.Index(fields=['company', 'status']),
            models.Index(fields=['code']),
        ]
        permissions = [
            ("can_change_status", "Can change location status"),
            ("can_mark_headquarters", "Can mark location as headquarters"),
        ]

    def __str__(self):
        return f"{self.company.name} - {self.name} ({self.get_status_display()})"

    def clean(self):
        """Custom validation"""
        # Check if another headquarters exists when setting is_headquarters
        if self.is_headquarters:
            exists = CompanyLocation.objects.filter(
                company=self.company,
                is_headquarters=True
            ).exclude(pk=self.pk).exists()
            if exists:
                raise ValidationError({
                    'is_headquarters': _('This company already has a headquarters location.')
                })
        
        # Validate operating hours format if provided
        if self.operating_hours:
            required_keys = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday'}
            if not all(day in self.operating_hours for day in required_keys):
                raise ValidationError({
                    'operating_hours': _('Operating hours must include all weekdays.')
                })

class LocationAuditLog(models.Model):
    """Model to track all changes to locations"""
    location = models.ForeignKey(
        CompanyLocation,
        on_delete=models.CASCADE,
        related_name='audit_logs'
    )
    action = models.CharField(max_length=50)  # 'create', 'update', 'delete'
    field_name = models.CharField(max_length=100, blank=True)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='location_audit_logs'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.location} - {self.action} by {self.user} at {self.timestamp}"
    

class Department(models.Model):
    # Basic Information
    Code =models.CharField(max_length=15,null=False,default="DEF")
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments')
    locations = models.ManyToManyField(CompanyLocation, related_name='departments')
    responsible_person = models.CharField(max_length=255, null=True, blank=True)
    is_main_department = models.BooleanField(default=False)
    
    # Department Options
    is_ipd = models.BooleanField(default=False, verbose_name=_("Is Internal Department (IPD)"))
    ipd_value_percentage = models.DecimalField(max_digits=5, decimal_places=2,default=0, null=True, blank=True,verbose_name=_("Internal Department (IPD) Rate for Services"))
    is_medical_package = models.BooleanField(default=False, verbose_name=_("Is Medical Package"))
    issue_inventory = models.BooleanField(default=False, verbose_name=_("Issue Inventory to Department"))
    is_laboratory = models.BooleanField(default=False, verbose_name=_("Is Laboratory Department"))
    laboratory_type_choices = [
        ('in-house', _('In-House')),
        ('outside', _('Outside')),
        ('partner_company', _('Partner Company')),
        ('sister_company', _('Sister Company')),
    ]
    laboratory_type = models.CharField(max_length=20, choices=laboratory_type_choices, null=True, blank=True)
    outside_value_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True,default=0, blank=True,verbose_name=_("Outside Commission Rate (%)"))
    is_operation_theater = models.BooleanField(default=False, verbose_name=_("Is Operation Theater"))
    operation_theater_date_mandatory = models.BooleanField(default=False, verbose_name=_("Is Date Mandatory for Operation Theater"))
    
    allow_discounts = models.BooleanField(default=False, verbose_name=_("Allow Discounts"))
    max_discount_percentage = models.DecimalField(max_digits=5, decimal_places=2,default=0, null=True, blank=True)
    
    income_account = models.CharField(max_length=255, null=True, blank=True)
    expense_account = models.CharField(max_length=255, null=True, blank=True)
    
    # Invoice and Sequence Options
    modify_invoice_number = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Invoice Number Modification"))
    issue_sequence_number = models.BooleanField(default=False, verbose_name=_("Issue Sequence Number"))
    issue_sequence_auto = models.BooleanField(default=True, verbose_name=_("Auto Sequence"))
    department_wise_sequence = models.BooleanField(default=False, verbose_name=_("Department Wise Sequence"))
    department_sequence_per_day = models.BooleanField(default=False, verbose_name=_("Department Sequence Per Day"))
    
    # Audit Fields
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='department_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='department_updated_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

 


class ClassDetail(models.Model):
    # Basic Information
    class_code = models.CharField(max_length=20, unique=True, verbose_name=_("Class Code"))
    name = models.CharField(max_length=255, verbose_name=_("Class Name"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))

    # Management Account Identification
    management_account_id = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Management Account ID"))
    accounting_enabled = models.BooleanField(default=False, verbose_name=_("Enable Accounting"))

    # Accounting Details
    income_account = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Income Account Reference"))
    expense_account = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Expense Account Reference"))
    max_posting_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Max Posting Limit"))

    # Relationships
    departments = models.ManyToManyField(Department, related_name='classesDepartments', verbose_name=_("Associated Departments"))

    # Status and Audit Fields
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='class_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='class_updated_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Class Detail")
        verbose_name_plural = _("Class Details")


class ClarificationDetail(models.Model):
    # Basic Information
    code = models.CharField(max_length=20, unique=True, verbose_name=_("Clarification Code"))
    name = models.CharField(max_length=255, verbose_name=_("Clarification Name"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))

    # Transaction Segregation
    is_income = models.BooleanField(default=False, verbose_name=_("Is Income Transaction"))
    is_expense = models.BooleanField(default=False, verbose_name=_("Is Expense Transaction"))
    is_adjustment = models.BooleanField(default=False, verbose_name=_("Is Adjustment Transaction"))

    # Advanced Options
    requires_approval = models.BooleanField(default=False, verbose_name=_("Requires Approval"))
    auto_post = models.BooleanField(default=False, verbose_name=_("Auto Post Transaction"))
    max_transaction_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name=_("Max Transaction Value"))

    # Relationships
    departments = models.ManyToManyField(Department, related_name='ClarificationDetailDepartments', verbose_name=_("Associated Departments"))

    # Audit Information
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clarification_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clarification_updated_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Clarification Detail")
        verbose_name_plural = _("Clarification Details")




class UserCompany(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users')
    
    class Meta:
        unique_together = ('user', 'company')
    
    def __str__(self):
        return f"{self.user.username} - {self.company.name}"

    
class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='userscompany')
    location = models.ForeignKey(CompanyLocation, on_delete=models.CASCADE, related_name='users')
    
    class Meta:
        unique_together = ('user', 'company', 'location')
    
    def __str__(self):
        return f"{self.user.username} - {self.company.name} - {self.location.name}"


class LaboratoryDepartment(models.Model):
    # Basic Information
    Code =models.CharField(max_length=15,null=False,default="DEF")
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='LaboratoryDepartments')
    locations = models.ManyToManyField(CompanyLocation, related_name='LaboratoryDepartmentdepartments')
    responsible_person = models.CharField(max_length=255, null=True, blank=True)
    is_main_department = models.BooleanField(default=False)
    
    laboratory_type_choices = [
        ('in-house', _('In-House')),
        ('outside', _('Outside')),
        ('partner_company', _('Partner Company')),
        ('sister_company', _('Sister Company')),
    ]
    laboratory_type = models.CharField(max_length=20, choices=laboratory_type_choices, null=True, blank=True)
    
    # Audit Fields
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='LaboratoryDepartmentdepartment_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='LaboratoryDepartmentdepartment_updated_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('Code', 'company')
    
    def __str__(self):
        return self.name


class TaxCode(models.Model):
    code = models.CharField(max_length=50, null=False)
    rate = models.DecimalField(max_digits=5, decimal_places=2,default=0)
    name = models.CharField(max_length=100)
    # status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    sequence = models.IntegerField(default=0)
    include_exclude = models.CharField(max_length=10, choices=[('Include', 'Include'), ('Exclude', 'Exclude')])
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='TaxCodecompany')
    locations = models.ManyToManyField(CompanyLocation, related_name='TaxCodelocations')

    # Audit Fields
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='TaxCode_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='TaxCode_updated_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

 
    class Meta:
        unique_together = ('code', 'company')
        verbose_name = "Tax Code"
        verbose_name_plural = "Tax Codes"

    def __str__(self):
        return self.code


 

class Service(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='service_company')
    locations = models.ManyToManyField('CompanyLocation', related_name='service_locations')
    departments = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='service_departments', verbose_name="Associated Departments")
    
    # Service details
    service_code = models.CharField(max_length=50, unique=True, verbose_name="Service Code")
    service_name = models.CharField(max_length=250, verbose_name="Service Name")
    rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Rate")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cost Price")
    minimum_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Minimum Price")
    item_barcode = models.CharField(max_length=100, verbose_name="Item Barcode")
    rate_per_day = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Rate Per Day")
    
    remarks = models.TextField(max_length=100,null=True, blank=True, default="", verbose_name="Remarks")
    
    # Laboratory-related fields
    laboratory_departments = models.ForeignKey('LaboratoryDepartment', on_delete=models.CASCADE,null=True,blank=True, related_name='laboratory_departments', verbose_name="Associated Laboratory Departments")
    print_lab_note = models.BooleanField(default=False, verbose_name="Print Laboratory Note")
    
    # Discount and diagnosis options
    highlight_in_diagnosis_sheet = models.BooleanField(default=False, verbose_name="Highlight in Diagnosis Sheet")
    allowed_discount = models.BooleanField(default=False, verbose_name="Allowed Discount")
    max_allowed_discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0, verbose_name="Max Allowed Discount (%)")
    
    # Tax-related fields
    tax_code = models.ManyToManyField('TaxCode',blank=True, related_name='service_taxes', verbose_name="Tax Code(s)")
    include_tax = models.BooleanField(default=False, verbose_name="Is Tax Included")
    
    # Audit Fields
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='service_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='service_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    # Meta class to enforce unique constraint and verbose naming
    class Meta:
        unique_together = ('service_code', 'company')
        verbose_name = "Service Registration"
        verbose_name_plural = "Service Registrations"
    
    def __str__(self):
        return self.service_name

class ServiceLocationPrice(models.Model):
    # Company and Location Information
    company = models.ForeignKey(
        'Company', 
        on_delete=models.CASCADE, 
        related_name='service_company_locations_price', 
        verbose_name="Company"
    )
    locations = models.ForeignKey(
        'CompanyLocation', 
        on_delete=models.CASCADE, 
        related_name='service_location_service', 
        verbose_name="Location"
    )
    service_code = models.ForeignKey(
        'Service', 
        on_delete=models.CASCADE, 
        related_name='service_location_price', 
        verbose_name="Service Code"
    )

    # Pricing Information
    rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Rate"
    )
    cost_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Cost Price"
    )
    minimum_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Minimum Price"
    )
    item_barcode = models.CharField(
        blank=True,
        max_length=100, 
        verbose_name="Item Barcode"
    )
    rate_per_day = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Rate Per Day"
    )

    # Additional Information
    remarks = models.TextField(
        max_length=100, 
        null=True, 
        blank=True, 
        default="", 
        verbose_name="Remarks"
    )

    # Laboratory-related fields
    print_lab_note = models.BooleanField(
        default=False, 
        verbose_name="Print Laboratory Note"
    )

    # Discount and Diagnosis Options
    allowed_discount = models.BooleanField(
        default=False, 
        verbose_name="Allowed Discount"
    )
    max_allowed_discount = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        default=0, 
        verbose_name="Max Allowed Discount (%)"
    )

    # Audit Fields
    is_active = models.BooleanField(
        default=True, 
        verbose_name="Is Active"
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='service_loc_price_created_by', 
        verbose_name="Created By"
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='service_loc_price_updated_by', 
        verbose_name="Updated By"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Created At"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Updated At"
    )

    # Meta Class
    class Meta:
        db_table = 'service_location_price'  # Custom table name (optional)
        unique_together = ('company', 'locations', 'service_code')
        verbose_name = "Service Location Price Registration"
        verbose_name_plural = "Service Location Price Registrations"

    def __str__(self):
        return f"{self.service_code} - {self.locations}"

class ServiceTax(models.Model):
    # Company and Location Information
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        related_name='service_tax_company',
        verbose_name="Company"
    )
    locations = models.ManyToManyField(
        'CompanyLocation',
        related_name='service_tax_locations',
        verbose_name="Locations"
    )
    service_code = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='service_tax_service',
        verbose_name="Service Code"
    )
    
    # Tax-related fields
    tax_code = models.ManyToManyField(
        'TaxCode',
        related_name='service_tax_codes',
        verbose_name="Tax Codes"
    )
    include_tax = models.BooleanField(
        default=False,
        verbose_name="Is Tax Included"
    )

    # Additional Information
    remarks = models.TextField(
        max_length=255,  # Increased max length for flexibility
        null=True,
        blank=True,
        default="",
        verbose_name="Remarks"
    )

    # Audit Fields
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='service_tax_created_by',
        verbose_name="Created By"
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='service_tax_updated_by',
        verbose_name="Updated By"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At"
    )

    # Meta Class
    class Meta:
        db_table = 'service_tax'
        verbose_name = "Service Tax Registration"
        verbose_name_plural = "Service Tax Registrations"

    def __str__(self):
        return f"{self.service_code} | {self.company}"



class ConsultationSupplierType(models.Model):
    Code = models.CharField(max_length=10, null=False)
    Description = models.CharField(max_length=100, null=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='SupplierTypecompany')
    locations = models.ManyToManyField(CompanyLocation, related_name='SupplierTypelocations')
    remarks = models.TextField(max_length=100,null=True, blank=True, default="", verbose_name="Remarks")
    # Audit Fields
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='SupplierType_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='SupplierType_updated_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

 
    class Meta:
        unique_together = ('Code', 'company')
        verbose_name = "Supplier Type"
        verbose_name_plural = "Supplier Type"

    def __str__(self):
        return self.Code


 


class SupplierRegistration(models.Model):
    # Company and Location Details

    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        related_name='supplier_registration_company',
        verbose_name="Default Company",
    )

    locations = models.ForeignKey(
        'CompanyLocation',
        on_delete=models.CASCADE,
        related_name='supplier_registration_locations',
        verbose_name="Default Location",
    )
    departments = models.ForeignKey(
        'Department',
        on_delete=models.CASCADE,
        related_name='supplier_departments',
        verbose_name="Default Department",
    )
    con_user_code = models.ForeignKey(
        'ConsultationSupplierType',
        on_delete=models.CASCADE,
        related_name='consultation_supplier_type',
        verbose_name="Consultation Type",
    )

    # Supplier Type Choices
    sup_type_choices = [
        ('1', _('Consultations (Doctor)')),
        ('2', _('Service Supplier')),
        ('3', _('Item Supplier')),
        ('4', _('MLT')),
        ('5', _('Other')),
    ]
    sup_type_sys_code = models.CharField(
        max_length=1,
        choices=sup_type_choices,
        default='1',
        verbose_name='Supplier Type',
    )

    # Basic Information
    sup_user_code = models.CharField(
        max_length=15,
        unique=True,
        verbose_name="Supplier User Code",
    )
    sup_titel = models.CharField(
        max_length=15,
        default="",
        verbose_name="Supplier Title",
    )
    gender_choices = [
        ('Male', _('Male')),
        ('Female', _('Female')),
        ('Other', _('Other')),
        ('Non', _('Non')),
    ]
    gender = models.CharField(
        max_length=15,
        choices=gender_choices,
        default='Non',
        verbose_name="Gender",
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date of Birth",
    )
    sup_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Supplier Name",
    )
    cheque_title = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Cheque Title",
    )
    contact_person = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Contact Person",
    )
    license_number = models.CharField(
        max_length=50,
        default="",
        verbose_name="License Number",
    )

    # Address Details
    add1 = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Address Line 1",
    )
    add2 = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Address Line 2",
    )
    add3 = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Address Line 3",
    )

    # Contact Details
    tel1 = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="Telephone 1",
    )
    tel2 = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="Telephone 2",
    )
    tele3 = models.CharField(
        max_length=15,
        default="",
        verbose_name="Telephone 3",
    )
    fax = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="Fax Number",
    )
    email = models.EmailField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Email Address",
    )
    web = models.URLField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Website URL",
    )

    # Tax and Financial Details
    full_acc_code = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="Full Account Code",
    )
    sub_acc_sys_code = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="Sub Account System Code",
    )
    edb_no = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="EDB Number",
    )
    vat_no = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="VAT Number",
    )
    tqb_no = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="TQB Number",
    )
    boi_no = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="BOI Number",
    )

    # Invoice and Settings
    invoice_code = models.CharField(
        max_length=5,
        default="",
        blank=True,
        verbose_name="Invoice Code",
    )
    inv_no_sup_wise = models.BooleanField(
        default=False,
        verbose_name="Department Wise Invoice Number",
    )
    dep_wise_sequence_no_yes = models.BooleanField(
        default=False,
        verbose_name="Department Wise Invoice Number Per Day",
    )
    e_channeling_ref_no = models.CharField(
        max_length=15,
        default="",
        blank=True,
        verbose_name="E-Channeling Reference Number",
    )

    # Withholding Tax
    app_wtax = models.BooleanField(
        default=False,
        verbose_name="App Withholding Tax",
    )
    app_wtax_pre = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        default=0,
        blank=True,
        verbose_name="App Withholding Tax %",
    )
    app_wtax_no = models.CharField(
        max_length=15,
        default="",
        blank=True,
        verbose_name="App Withholding Tax Number",
    )
    sms_name = models.CharField(
        max_length=200,
        default="",
        verbose_name="Digital SMS Name",
    )

    # Miscellaneous
    remarks = models.CharField(
        max_length=250,
        default="",
        null=True, blank=True,
        verbose_name="Remarks",
    )
    acc_head_code = models.CharField(
        max_length=25,
        default="",
        verbose_name="Account Head Code",
    )
    acc_code = models.CharField(
        max_length=25,
        default="",
        verbose_name="Account Code",
    )

        # Audit Fields
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='supplier_registration_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='supplier_registration_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        db_table = 'supplier_registration'
        verbose_name = "Supplier Registration"
        verbose_name_plural = "Supplier Registrations"
        unique_together = ('company', 'sup_user_code')

    def __str__(self):
        return f"{self.sup_name} ({self.sup_user_code})"



 

class SupplierDepartmentDetails(models.Model):
    # Company and Location Details
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        related_name='supplier_registration_company_department',
        verbose_name="Company",
    )
    locations = models.ForeignKey(
        'CompanyLocation',
        on_delete=models.CASCADE,
        related_name='supplier_registration_locations_department',
        verbose_name="Location",
    )

    # Supplier Information
    supplier = models.ForeignKey(
        'SupplierRegistration',
        on_delete=models.CASCADE,
        related_name='supplier_details',
        verbose_name="Supplier",
    )

    # Department Information
    departments = models.ForeignKey(
        'Department',
        on_delete=models.CASCADE,
        related_name='supplier_department_details_departments',
        verbose_name="Associated Departments",
    )

    # Service Information
    services_code = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='supplier_department_service_details',
        verbose_name="Services Code",
    )
    hospital_services_code = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='supplier_department_hospital_services_code',
        verbose_name="Hospital Services Code",
    )

    # Rates and Fees
    channeling_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Channeling Rate",
        blank=True,
        null=True,
    )
    hospital_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Hospital Rate",
        blank=True,
        null=True,
    )
    rate_cost_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Rate (Cost) per Day",
        blank=True,
        null=True,
    )
    is_doctor_fees = models.BooleanField(
        default=False,
        verbose_name="Is Doctor Fees",
    )

    # Appointment Details
    number_of_appointments = models.PositiveIntegerField(
        default=0,
        verbose_name="Number of Appointments",
    )
    appointment_duration = models.DurationField(
        verbose_name="Appointment Duration (HH:MM)",
        blank=True,
        null=True,
    )

    # Audit Fields
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='supplier_department_created_by',
        verbose_name="Created By",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='supplier_department_updated_by',
        verbose_name="Updated By",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
    )

    class Meta:
        db_table = 'supplier_department_details'
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'locations', 'supplier', 'departments'],
                name='unique_supplier_department_details'
            ),
        ]
        verbose_name = "Supplier Department Detail"
        verbose_name_plural = "Supplier Department Details"

    def __str__(self):
        return f"{self.supplier} - {self.departments} - {self.services_code}"


class SupplierReferralFeeDetails(models.Model):
    # Company and Location Details
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        related_name='supplier_registration_ReferralFee',
        verbose_name="Company",
    )
    locations = models.ForeignKey(
        'CompanyLocation',
        on_delete=models.CASCADE,
        related_name='supplier_ReferralFee_locations_department',
        verbose_name="Location",
    )

    # Supplier Information
    supplier = models.ForeignKey(
        'SupplierRegistration',
        on_delete=models.CASCADE,
        related_name='supplier_detailsReferralFee',
        verbose_name="Supplier",
    )

    # Department Information
    departments = models.ForeignKey(
        'Department',
        on_delete=models.CASCADE,
        related_name='supplier_ReferralFee_details_departments',
        verbose_name="Associated Departments",
    )

    # Service Information
    services_code = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='supplier_ReferralFee_service_details',
        verbose_name="Services Code",
    )
    
    # Rates and Fees
    ReferralFee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Referral Fee Amount",
        blank=True,
        null=True,
    )
    ReferralFeePre = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Referral Fee %",
        blank=True,
        null=True,
    )
    

    # Audit Fields
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='supplier_ReferralFee_created_by',
        verbose_name="Created By",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='supplier_ReferralFee_updated_by',
        verbose_name="Updated By",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
    )

    class Meta:
        db_table = 'supplier_ReferralFee_details'
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'locations', 'supplier', 'departments','services_code'],
                name='unique_supplier_ReferralFee_details'
            ),
        ]
        verbose_name = "Supplier ReferralFee Detail"
        verbose_name_plural = "Supplier ReferralFee Details"

    def __str__(self):
        return f"{self.supplier} - {self.departments} - {self.services_code}"

