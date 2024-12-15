# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CompanyForm
from .models import Company

@login_required
def company_create(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.created_by = request.user
            company.updated_by = request.user
            company.save()
            messages.success(request, 'Company created successfully.')
            return redirect('company_detail', pk=company.pk)
    else:
        form = CompanyForm()
    
    return render(request, 'companies/company_form.html', {'form': form})

@login_required
def company_edit(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            company = form.save(commit=False)
            company.updated_by = request.user
            company.save()
            messages.success(request, 'Company updated successfully.')
            return redirect('company_detail', pk=company.pk)
    else:
        form = CompanyForm(instance=company)
    
    return render(request, 'companies/company_form.html', {
        'form': form,
        'company': company
    })

@login_required
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'companies/company_list.html', {'companies': companies})

@login_required
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    return render(request, 'companies/company_detail.html', {'company': company})

# from rest_framework import serializers
# from .models import SupplierReferralFeeDetails

# class SupplierReferralFeeDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SupplierReferralFeeDetails
#         fields = '__all__'
