# Generated by Django 5.1.3 on 2024-11-24 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0031_supplierdepartmentdetails'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='supplierdepartmentdetails',
            unique_together={('company', 'locations', 'supplier', 'departments')},
        ),
    ]
