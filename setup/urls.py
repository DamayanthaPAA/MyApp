# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('company/', views.company_list, name='company_list'),
    path('company/create/', views.company_create, name='company_create'),
    path('company/<int:pk>/', views.company_detail, name='company_detail'),
    path('company/<int:pk>/edit/', views.company_edit, name='company_edit'),
]