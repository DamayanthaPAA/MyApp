# Generated by Django 5.1.3 on 2024-11-24 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0014_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='allowed_discount',
            field=models.BooleanField(default=False, verbose_name='Allowed Discount'),
        ),
        migrations.AlterField(
            model_name='service',
            name='cost_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Cost Price'),
        ),
        migrations.AlterField(
            model_name='service',
            name='include_tax',
            field=models.BooleanField(default=False, verbose_name='Is Tax Inclide'),
        ),
        migrations.AlterField(
            model_name='service',
            name='item_barcode',
            field=models.CharField(max_length=100, verbose_name='Barcode'),
        ),
        migrations.AlterField(
            model_name='service',
            name='minimum_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Minimum Price'),
        ),
        migrations.AlterField(
            model_name='service',
            name='print_lab_note',
            field=models.BooleanField(default=False, verbose_name='Print Laboratory Note'),
        ),
        migrations.AlterField(
            model_name='service',
            name='rate',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Rate'),
        ),
        migrations.AlterField(
            model_name='service',
            name='rate_per_day',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Rate Per Day'),
        ),
        migrations.AlterField(
            model_name='service',
            name='remarks',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Remarks'),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_Name',
            field=models.CharField(max_length=250, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_code',
            field=models.CharField(max_length=50, verbose_name='Code'),
        ),
    ]