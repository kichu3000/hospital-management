from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    USER_TYPE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    ]
    GENDER = [
        ('male','Male'),
        ('female','Female'),
        ('Unknown','Unknown')
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=3)
    user_type = models.CharField(max_length=7, choices=USER_TYPE_CHOICES)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    last_login = models.DateTimeField(auto_now=True,null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    adress = models.CharField(max_length=100, default='Unknown')
    gender = models.CharField(max_length=10, choices=GENDER, default='Unknown')
    date_of_birth = models.DateField(null=True, blank=True)  # Allow null and blank values

    # Custom manager
    objects = UserManager()

    # The field that will be used to authenticate users
    USERNAME_FIELD = 'email'

    # Fields required for creating a superuser
    REQUIRED_FIELDS = ['name', 'phone', 'user_type']

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        # Password is already hashed by default, you don't need to store it manually.
        super().set_password(raw_password)

    def check_password(self, raw_password):
        # Check password against the hashed password stored by default.
        return super().check_password(raw_password)

class appointment(models.Model):
    patient_name = models.CharField(max_length=255)
    doctor_name = models.CharField(max_length=255, default='Unknown Doctor') 
    date = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    Symptoms = models.TextField()

    def __str__(self):
        return f'{self.patient_name} - {self.doctor_name} on {self.date}'
