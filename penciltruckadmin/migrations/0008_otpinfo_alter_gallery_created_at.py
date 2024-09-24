# Generated by Django 5.0 on 2024-09-24 12:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('penciltruckadmin', '0007_remove_volunteer_bio_remove_volunteer_role_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtpInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('email_otp', models.CharField(max_length=15)),
                ('phone', models.CharField(max_length=15)),
                ('phone_otp', models.CharField(max_length=15)),
            ],
        ),
        migrations.AlterField(
            model_name='gallery',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 24, 12, 41, 50, 100646, tzinfo=datetime.timezone.utc)),
        ),
    ]
