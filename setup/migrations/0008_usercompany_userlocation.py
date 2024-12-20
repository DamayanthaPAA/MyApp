# Generated by Django 5.1.3 on 2024-11-24 18:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0007_clarificationdetail_classdetail'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='setup.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companies', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'company')},
            },
        ),
        migrations.CreateModel(
            name='UserLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userscompany', to='setup.company')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='setup.companylocation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'company', 'location')},
            },
        ),
    ]
