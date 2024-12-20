# Generated by Django 5.1.3 on 2024-11-25 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0043_alter_servicetax_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplierregistration',
            name='e_channeling_ref_no',
            field=models.CharField(blank=True, default='', max_length=15, verbose_name='E-Channeling Reference Number'),
        ),
        migrations.AlterField(
            model_name='supplierregistration',
            name='invoice_code',
            field=models.CharField(blank=True, default='', max_length=5, verbose_name='Invoice Code'),
        ),
        migrations.AlterField(
            model_name='supplierregistration',
            name='web',
            field=models.URLField(blank=True, default='', max_length=100, verbose_name='Website URL'),
        ),
    ]
