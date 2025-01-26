# Generated by Django 5.1.2 on 2025-01-26 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_alter_appointment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('upcoming', 'Upcoming'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='upcoming', max_length=10),
        ),
    ]
