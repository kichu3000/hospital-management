from django.shortcuts import render, redirect
from . forms import SignUpForm
from django.contrib import messages  # For user feedback
from django.db import IntegrityError  # For database errors

from django.contrib.auth import authenticate, login
from .models import User, appointment
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
# def home(request):
#     return render(request,'home.html')




def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        blood_group = request.POST.get('blood_group')
        user_type = request.POST.get('user_type')
        specialization = request.POST.get('specialization') # Only for doctors


        # Validate password confirmation
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        # Save the data to the database
        hash_password =make_password(password1)  # In production, hash the password
        try:
            # Try to create a new user in the database
            User.objects.create(
                name=name,
                email=email,
                phone=phone,
                password=hash_password,  # In production, store hashed passwords
                blood_group=blood_group,
                specialization=specialization,
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
            print(user.password)
        except User.DoesNotExist:
            user = None

        if user is not None and check_password(password, user.password):
            # print(user.password)
            # Login the user
            print("User ----------------------------------",user)
            login(request, user)
            
            messages.success(request, "Login successful!")
            # doctors = get_doctors()  # Get the list of doctors
            # print("Doctor present ",doctors)
            return redirect('dashboard')  # Redirect to dashboard or home page
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect('login')  # Re-render login page with error

    return render(request, 'login.html')




def dashboard(request):
    pass




#To get all the doctors from the database, we can create a helper function in views.py:
def get_doctors():
    doctors = User.objects.filter(user_type='doctor')
    return doctors



def book_appointment(request):
    doctors = get_doctors()  # Get the list of doctors
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')  # Patient's name entered by the user
        doctor_name = request.POST.get('doctor')  # Doctor's name selected from the dropdown
        email = request.POST.get('patient_email')  # Email entered by the user
        phone = request.POST.get('patient_phone')  # Phone number entered by the user
        symptoms = request.POST.get('symptoms')  # Symptoms entered by the user
        date = request.POST.get('date')

        # For testing
        print("Patient name:", patient_name)
        print("Doctor ID:", doctor_name)
        print("Date:", date)
        print("Email:", email)
        print("Phone:", phone)
        print("Symptoms:", symptoms)

        try:
            # Check if the email exists in the database
            patient_exists = User.objects.filter(email=email).exists()
            if not patient_exists:
                messages.error(request, "No account found with this email. Please create an account.")
                return redirect('signup')  # Redirect to the signup page  # Get the Patient object by email
            print("Patient found:", patient_exists)
            # Create the appointment
            appointment.objects.create(
                patient_name=patient_name,
                doctor_name=doctor_name,  # Store doctor by ID directly
                date=date,
                email=email,
                phone=phone,
                Symptoms=symptoms
            )
            messages.success(request, "Appointment booked successfully!")
            return redirect('book_appointment')  # Redirect to the appointment page

        except User.DoesNotExist:
            # If email doesn't exist, ask the user to create an account
            messages.error(request, "No account found with this email. Please create an account.")
            return redirect('signup')  # Redirect to the signup page

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('book_appointment')  # Redirect back in case of any other error

    return render(request, 'home.html', {'doctors': doctors})


def doctor(request):
    doctors = get_doctors()  # Get the list of doctors
    return render(request, 'doctors.html', {'doctors': doctors})