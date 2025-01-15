# Generated by Django 5.1.2 on 2025-01-15 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_appointment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='patient',
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor_name',
            field=models.CharField(default='Unknown doctor', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient_name',
            field=models.CharField(default='Unknown Doctor', max_length=255),
            preserve_default=False,
        ),
    ]
