# class SupplierRegistration(models.Model):
#     company = models.ManyToManyField(Company,  related_name='SupplierRegistrationcompany')
#     locations = models.ForeignKey(CompanyLocation, related_name='SupplierRegistrationlocations', verbose_name='Default Location')
    
#     departments = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='Supplierservice_departments', verbose_name="Default Department")
#     con_user_code = models.ForeignKey('ConsultationSupplierType', on_delete=models.CASCADE, related_name='ConsultationSupplierTypeSupplierservice', verbose_name="Type")
#     sup_type_choices = [
#         ('1', _('Consultations (Doctor)')),
#         ('2', _('Service Supplier')),
#         ('3', _('Item Supplier')),
#         ('4', _('MLT')),
#         ('5', _('Other')),
#     ]
#     sup_type_sys_code = models.IntegerChoices(choices=sup_type_choices ,default=1, verbose_name='Supplier Type')
    
#     sup_user_code = models.CharField(
#         max_length=15, 
#         verbose_name="Supplier User Code"
#     )
#     sup_titel = models.CharField(
#         max_length=15, 
#         default="", 
#         verbose_name="Supplier Title"
#     )
#     gender_choices = [
#         ('Male', _('Male')),
#         ('Female', _('Female')),
#         ('Other', _('Other')),
#         ('Non', _('Non')),
#     ]
#     gender = models.CharField(
#         max_length=15, 
#         default="Non", choices=gender_choices ,
#         verbose_name="Gender"
#     )
#     date_of_birth = models.DateTimeField(
#         default="CURRENT_TIMESTAMP", 
#         verbose_name="Date of Birth"
#     )
#     sup_name = models.CharField(
#         max_length=100, 
#         null=True, 
#         blank=True, 
#         verbose_name="Supplier Name"
#     )
#     cheque_title = models.CharField(
#         max_length=100, 
#         null=True, 
#         blank=True, 
#         verbose_name="Cheque Title"
#     )
#     contact_person = models.CharField(
#         max_length=100, 
#         null=True, 
#         blank=True, 
#         verbose_name="Contact Person"
#     )
#     license_number = models.CharField(
#         max_length=50, 
#         default="", 
#         verbose_name="License Number"
#     )
#     add1 = models.CharField(
#         max_length=100, 
#         null=True, 
#         blank=True, 
#         verbose_name="Address Line 1"
#     )
#     add2 = models.CharField(
#         max_length=100, 
#         null=True, 
#         blank=True, 
#         verbose_name="Address Line 2"
#     )
#     add3 = models.CharField(
#         max_length=100, 
#         null=True, 
#         blank=True, 
#         verbose_name="Address Line 3"
#     )
#     tel1 = models.CharField(
#         max_length=15, 
#         null=True, 
#         blank=True, 
#         verbose_name="Telephone 1"
#     )
#     tel2 = models.CharField(
#         max_length=15, 
#         null=True, 
#         blank=True, 
#         verbose_name="Telephone 2"
#     )
#     tele3 = models.CharField(
#         max_length=15, 
#         default="", 
#         verbose_name="Telephone 3"
#     )
#     fax = models.CharField(
#         max_length=15, 
#         null=True, 
#         blank=True, 
#         verbose_name="Fax Number"
#     )
#     email = models.CharField(
#         max_length=100, 
#         null=True, 
#         blank=True, 
#         verbose_name="Email Address"
#     )

#     web = models.CharField(
#         max_length=100, 
#         default="", 
#         verbose_name="Website URL"
#     )
#     full_acc_code = models.CharField(
#         max_length=10, 
#         null=True, 
#         blank=True, 
#         verbose_name="Full Account Code"
#     )
#     sub_acc_sys_code = models.CharField(
#         max_length=10, 
#         null=True, 
#         blank=True, 
#         verbose_name="Sub Account System Code"
#     )

#     edb_no = models.CharField(
#         max_length=50, 
#         null=True, 
#         blank=True, 
#         verbose_name="EDB Number"
#     )
#     vat_no = models.CharField(
#         max_length=50, 
#         null=True, 
#         blank=True, 
#         verbose_name="VAT Number"
#     )
#     tqb_no = models.CharField(
#         max_length=50, 
#         null=True, 
#         blank=True, 
#         verbose_name="TQB Number"
#     )
#     boi_no = models.CharField(
#         max_length=50, 
#         null=True, 
#         blank=True, 
#         verbose_name="BOI Number"
#     )

 
#     remarks = models.CharField(
#         max_length=250, 
#         default="", 
#         verbose_name="Remarks"
#     )
#     acc_head_code = models.CharField(
#         max_length=25, 
#         default="", 
#         verbose_name="Account Head Code"
#     )
#     acc_code = models.CharField(
#         max_length=25, 
#         default="", 
#         verbose_name="Account Code"
#     )
 
#     invoice_code = models.CharField(
#         max_length=2, 
#         default="", 
#         verbose_name="Invoice Code"
#     )
#     inv_no_sup_wise =models.BooleanField(default=False, 
#         verbose_name="Department Wise Invoice Number"
#     )
#     dep_wise_sequence_no_yes = models.BooleanField(default=False,      
#         verbose_name="Department Wise Invoice Number Per Day"
#     )
#     e_channeling_ref_no = models.CharField(
#         max_length=15, 
#         default="", 
#         verbose_name="E-Channeling Reference Number"
#     )
 
#     app_wtax = models.BooleanField(
#         default=False, 
#         verbose_name="App Withholding Tax"
#     )
#     app_wtax_pre = models.DecimalField(
#         max_digits=10, 
#         decimal_places=3, 
#         default=0, 
#         verbose_name="App Withholding Tax %"
#     )
#     app_wtax_no = models.CharField(
#         max_length=15, 
#         default="", 
#         verbose_name="App Withholding Tax Number"
#     )
#     sms_name = models.CharField(
#         max_length=200, 
#         default="", 
#         verbose_name="Digital SMS Name"
#     )

#     class Meta:
#         db_table = 'Cr_SupplierRegistration_tab'
#         verbose_name = "Supplier Registration"
#         verbose_name_plural = "Supplier Registrations"
#         unique_together = ('comp_code', 'sup_user_code')
        

#     def __str__(self):
#         return f"{self.sup_name} ({self.sup_user_code})"





# -----------------------
# class SupplierRegistration(models.Model):
#     company = models.ManyToManyField(Company,  related_name='SupplierRegistrationcompany')
#     # locations = models.ManyToManyField(CompanyLocation, related_name='SupplierRegistrationlocations')
    
#     departments = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='Supplierservice_departments', verbose_name="Default Department")
#     con_user_code = models.ForeignKey('ConsultationSupplierType', on_delete=models.CASCADE, related_name='ConsultationSupplierTypeSupplierservice', verbose_name="Type")
#     sup_type_choices = [
#         ('1', _('Consultations (Doctor)')),
#         ('2', _('Service Supplier')),
#         ('3', _('Item Supplier')),
#         ('4', _('MLT')),
#         ('5', _('Other')),
#     ]
#     sup_type_sys_code = models.IntegerChoices(choices=sup_type_choices ,default=1, verbose_name='Supplier Type')
    
#     sup_user_code = models.CharField(
#         max_length=15, 
#         verbose_name="Supplier User Code"
#     )
#     sup_titel = models.CharField(
#         max_length=15, 
#         default="", 
#         verbose_name="Supplier Title"
#     )
#     gender_choices = [
#         ('Male', _('Male')),
#         ('Female', _('Female')),
#         ('Other', _('Other')),
#         ('Non', _('Non')),
#     ]
#     gender = models.CharField(
#         max_length=15, 
#         default="Non", choices=gender_choices ,
#         verbose_name="Gender"
#     )
#     date_of_birth = models.DateTimeField(
#         default="CURRENT_TIMESTAMP", 
#         verbose_name="Date of Birth"
#     )
#     sup_name = models.CharField(
#         max_length=100, 
#         null=True, 
#         blank=True, 
#         verbose_name="Supplier Name"
#     )
#     cheque_title = models.CharField(
#         max_length=100, 
#         null=True, 
#         blank=True, 
#         verbose_name="Cheque Title"
#     )
#     contact_person = models.CharField(
#         max_length=100, 
#         null=True, 
#         blank=True, 
#         verbose_name="Contact Person"
#     )
#     license_number = models.CharField(
#         max_length=50, 
#         default="", 
#         verbose_name="License Number"
#     )
#     add1 = models.CharField(
#         max_length=100, 
#         null=True, 
#         blank=True, 
#         verbose_name="Address Line 1"
#     )
#     add2 = models.CharField(
#         max_length=100, 
#         null=True, 
#         blank=True, 
#         verbose_name="Address Line 2"
#     )
#     add3 = models.CharField(
#         max_length=100, 
#         null=True, 
#         blank=True, 
#         verbose_name="Address Line 3"
#     )
#     tel1 = models.CharField(
#         max_length=15, 
#         null=True, 
#         blank=True, 
#         verbose_name="Telephone 1"
#     )
#     tel2 = models.CharField(
#         max_length=15, 
#         null=True, 
#         blank=True, 
#         verbose_name="Telephone 2"
#     )
#     tele3 = models.CharField(
#         max_length=15, 
#         default="", 
#         verbose_name="Telephone 3"
#     )
#     fax = models.CharField(
#         max_length=15, 
#         null=True, 
#         blank=True, 
#         verbose_name="Fax Number"
#     )
#     email = models.CharField(
#         max_length=100, 
#         null=True, 
#         blank=True, 
#         verbose_name="Email Address"
#     )

#     web = models.CharField(
#         max_length=100, 
#         default="", 
#         verbose_name="Website URL"
#     )
#     full_acc_code = models.CharField(
#         max_length=10, 
#         null=True, 
#         blank=True, 
#         verbose_name="Full Account Code"
#     )
#     sub_acc_sys_code = models.CharField(
#         max_length=10, 
#         null=True, 
#         blank=True, 
#         verbose_name="Sub Account System Code"
#     )

#     edb_no = models.CharField(
#         max_length=50, 
#         null=True, 
#         blank=True, 
#         verbose_name="EDB Number"
#     )
#     vat_no = models.CharField(
#         max_length=50, 
#         null=True, 
#         blank=True, 
#         verbose_name="VAT Number"
#     )
#     tqb_no = models.CharField(
#         max_length=50, 
#         null=True, 
#         blank=True, 
#         verbose_name="TQB Number"
#     )
#     boi_no = models.CharField(
#         max_length=50, 
#         null=True, 
#         blank=True, 
#         verbose_name="BOI Number"
#     )


     
#     # rate = models.DecimalField(
#     #     max_digits=18, 
#     #     decimal_places=2, 
#     #     default=0, 
#     #     verbose_name="Rate"
#     # )
#     # channeling_rate = models.DecimalField(
#     #     max_digits=18, 
#     #     decimal_places=2, 
#     #     default=0, 
#     #     verbose_name="Channeling Rate"
#     # )
#     # appointment_duration = models.DecimalField(
#     #     max_digits=18, 
#     #     decimal_places=2, 
#     #     default=0, 
#     #     verbose_name="Appointment Duration"
#     # )
#     # referring_charges = models.DecimalField(
#     #     max_digits=18, 
#     #     decimal_places=2, 
#     #     default=0, 
#     #     verbose_name="Referring Charges"
#     # )
#     # ser_user_code = models.CharField(
#     #     max_length=10, 
#     #     default="", 
#     #     verbose_name="Service User Code"
#     # )
#     remarks = models.CharField(
#         max_length=250, 
#         default="", 
#         verbose_name="Remarks"
#     )
#     acc_head_code = models.CharField(
#         max_length=25, 
#         default="", 
#         verbose_name="Account Head Code"
#     )
#     acc_code = models.CharField(
#         max_length=25, 
#         default="", 
#         verbose_name="Account Code"
#     )
#     # is_doctor_fees = models.CharField(
#     #     max_length=1, 
#     #     default="", 
#     #     verbose_name="Is Doctor Fees"
#     # )
#     # user_sys_code = models.CharField(
#     #     max_length=4, 
#     #     null=True, 
#     #     blank=True, 
#     #     verbose_name="User System Code"
#     # )
#     # hospital_service_code = models.CharField(
#     #     max_length=15, 
#     #     default="", 
#     #     verbose_name="Hospital Service Code"
#     # )
#     # hospital_rate = models.DecimalField(
#     #     max_digits=18, 
#     #     decimal_places=2, 
#     #     default=0, 
#     #     verbose_name="Hospital Rate"
#     # )
#     invoice_code = models.CharField(
#         max_length=2, 
#         default="", 
#         verbose_name="Invoice Code"
#     )
#     inv_no_sup_wise =models.BooleanField(default=False, 
#         verbose_name="Department Wise Invoice Number"
#     )
#     dep_wise_sequence_no_yes = models.BooleanField(default=False,      
#         verbose_name="Department Wise Invoice Number Per Day"
#     )
#     e_channeling_ref_no = models.CharField(
#         max_length=15, 
#         default="", 
#         verbose_name="E-Channeling Reference Number"
#     )
#     # no_of_appointments = models.IntegerField(
#     #     default=100, 
#     #     verbose_name="Number of Appointments"
#     # )
#     app_wtax = models.BooleanField(
#         default=False, 
#         verbose_name="App Withholding Tax"
#     )
#     app_wtax_pre = models.DecimalField(
#         max_digits=10, 
#         decimal_places=3, 
#         default=0, 
#         verbose_name="App Withholding Tax %"
#     )
#     app_wtax_no = models.CharField(
#         max_length=15, 
#         default="", 
#         verbose_name="App Withholding Tax Number"
#     )
#     sms_name = models.CharField(
#         max_length=200, 
#         default="", 
#         verbose_name="Digital SMS Name"
#     )

#     class Meta:
#         db_table = 'Cr_SupplierRegistration_tab'
#         verbose_name = "Supplier Registration"
#         verbose_name_plural = "Supplier Registrations"
#         unique_together = ('comp_code', 'sup_user_code')
#         # constraints = [
#         #     models.CheckConstraint(check=models.Q(app_wtax__in=[True, False]), name="check_app_wtax_boolean"),
#         # ]

#     def __str__(self):
#         return f"{self.sup_name} ({self.sup_user_code})"
