from django.db import models

# Create your models here.

class User(models.Model):
    USER_TYPE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3)
    user_type = models.CharField(max_length=7, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.name