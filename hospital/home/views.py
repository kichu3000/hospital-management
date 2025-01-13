from django.shortcuts import render, redirect
from . forms import SignUpForm
from django.contrib import messages  # For user feedback
from django.db import IntegrityError  # For database errors

from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User

from .models import User
# Create your views here.
def home(request):
    return render(request,'home.html')




def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        blood_group = request.POST.get('blood_group')
        user_type = request.POST.get('user_type')

        # Validate password confirmation
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        # Save the data to the database
        try:
            # Try to create a new user in the database
            User.objects.create(
                name=name,
                email=email,
                phone=phone,
                password=password1,  # In production, store hashed passwords
                blood_group=blood_group,
                user_type=user_type
            )
            messages.success(request, "Sign-up successful!")
            return redirect('signup')  # Redirect to a success page or homepage

        except IntegrityError as e:
            # Check if the error is caused by duplicate email
            if 'email' in str(e):
                messages.error(request, "This email is already used. Please try a different one.")
            else:
                # If some other error occurs, display a generic error message
                messages.error(request, "An error occurred. Please try again later.")
            return redirect('signup')

    return render(request, 'signup.html')



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Get the email from the form
        password = request.POST.get('password')  # Get the password from the form

        # Authenticate user
        try:
            # Find the user by email
            user = User.objects.get(email=email)
            # print(user.email)
            # print(user.password)
        except User.DoesNotExist:
            user = None

        if user is not None and user.password == password:
            # print(user.password)
            # Login the user
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')  # Redirect to dashboard or home page
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect('login')  # Re-render login page with error

    return render(request, 'login.html')


def dashboard(request):
    pass