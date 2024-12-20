# Generated by Django 5.1.3 on 2024-11-24 20:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0018_alter_service_tax_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='laboratory_departments',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='laboratory_departments', to='setup.laboratorydepartment', verbose_name='Associated Laboratory Departments'),
        ),
        migrations.AlterField(
            model_name='service',
            name='tax_code',
            field=models.ManyToManyField(blank=True, null=True, related_name='service_taxes', to='setup.taxcode', verbose_name='Tax Code(s)'),
        ),
    ]
