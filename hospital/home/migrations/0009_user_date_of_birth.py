# Generated by Django 5.1.2 on 2025-01-21 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_user_adress_user_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default='2000-01-01'),
        ),
    ]
