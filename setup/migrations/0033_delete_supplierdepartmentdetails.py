# Generated by Django 5.1.3 on 2024-11-24 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0032_alter_supplierdepartmentdetails_unique_together'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SupplierDepartmentDetails',
        ),
    ]