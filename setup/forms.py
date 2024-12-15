# forms.py
from django import forms
from .models import Company
from .models import Department
from .models import LaboratoryDepartment

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['created_by', 'updated_by']  # These will be set automatically

 


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class LaboratoryDepartmentForm(forms.ModelForm):
    class Meta:
        model = LaboratoryDepartment
        fields = '__all__'


from .models import ClassDetail

class ClassDetailForm(forms.ModelForm):
    class Meta:
        model = ClassDetail
        fields = '__all__'


 
from .models import ClarificationDetail

class ClarificationDetailForm(forms.ModelForm):
    class Meta:
        model = ClarificationDetail
        fields = '__all__'
