# Generated by Django 5.1.3 on 2024-11-25 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0044_alter_supplierregistration_e_channeling_ref_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplierregistration',
            name='app_wtax_no',
            field=models.CharField(blank=True, default='', max_length=15, verbose_name='App Withholding Tax Number'),
        ),
        migrations.AlterField(
            model_name='supplierregistration',
            name='app_wtax_pre',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=10, verbose_name='App Withholding Tax %'),
        ),
    ]
