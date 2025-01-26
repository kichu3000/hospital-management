from django.shortcuts import render, redirect
from . forms import SignUpForm
from django.contrib import messages  # For user feedback
from django.db import IntegrityError  # For database errors

from django.contrib.auth import  login,logout
from .models import User, appointment, Prescription
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime
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
            isSameday = appointment.objects.filter(date=date).exists()

            if not patient_exists:
                messages.error(request, "No account found with this email. Please create an account.")
                return redirect('signup')  # Redirect to the signup page  # Get the Patient object by email
            if isSameday:
                messages.error(request,"You already have an appointment booked on the same day. You cannot book two appointments on the same day.")
                return redirect('signup')
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
    logout(request)  # Clear session data
    return render(request, 'home.html', {'doctors': doctors})



def get_doctors():
    doctors = User.objects.filter(user_type='doctor')
    return doctors


def doctor(request):
    doctors = get_doctors()  # Get the list of doctors
    logout(request)  # Clear session data
    return render(request, 'doctors.html', {'doctors': doctors})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Get the email from the form
        password = request.POST.get('password')  # Get the password from the form

        # Authenticate user
        try:
            user = User.objects.get(email=email)  # Find the user by email
        except User.DoesNotExist:
            user = None

        if user is not None and check_password(password, user.password):
            login(request, user)  # Login the user
            # print("Session data after login:", request.session.items())

            messages.success(request, "Login successful!")
        
            
            request.session['user_name'] = user.name
            request.session['user_email'] = user.email
            request.session['is_authenticated'] = user.is_authenticated
            request.session['user_type'] = user.user_type
            request.session['user_phone'] = user.phone
            request.session['blood_group'] = user.blood_group
            request.session['date_of_birth'] = user.date_of_birth.strftime('%Y-%m-%d')  # Serialize date
            request.session['gender'] = user.gender
            request.session['address'] = user.address
            request.session['specialization'] = user.specialization


            if user.user_type == 'doctor':
                print("Redirecting to doctor dashboard")

               
                
                return redirect('doctor_dashboard')  # Ensure this matches the name in urls.py
            elif user.user_type == 'patient':
                # print("Session Key:", request.session.session_key)
                # print("User Authenticated:", request.user.is_authenticated)

                print("Redirecting to user dashboard")


                return redirect('user_dashboard')  # Ensure this matches the name in urls.py
            else:
                return redirect('admin_dashboard')  # Ensure this matches the name in urls.py

        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect('login')  # Re-render login page with error

    print("Rendering login page")
    return render(request, 'login.html')  # Render login page for GET requests







def user_dashboard(request):
    # Get session data manually

    user_email = request.session.get('user_email')
    user_name = request.session.get('user_name')
    user_type = request.session.get('user_type')
    is_authenticated = request.session.get('is_authenticated')
    user_phone = request.session.get('user_phone')
    blood_group = request.session.get('blood_group')
    date_of_birth = request.session.get('date_of_birth')
    gender = request.session.get('gender')
    address = request.session.get('address')



 

    # Check if the user is authenticated
    if not is_authenticated:
        return HttpResponse("You are not logged in.", status=401)  # Handle unauthenticated users
    
    appointments = appointment.objects.filter(email=user_email)  # Get the user's appointments

  # Get the current date
    past_appointments = appointments.filter(status='completed')  # Get past appointments
    upcoming_appointments = appointments.filter(status='upcoming')  # Get upcoming appointments

    # Use these details in the view
    context = {
        'user_name': user_name,
        'user_email': user_email,
        'user_type': user_type,
        'user_phone': user_phone,
        'blood_group': blood_group,
        'dob': date_of_birth,
        'gender' : gender,
        'address' : address,
        'past_appointments': past_appointments,
        'upcoming_appointments': upcoming_appointments,
        # 'prescription': prescription,
    }

    return render(request, 'user_dashboard.html', context)






def update_profile(request):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('login')  # Redirect to login page if user is not logged in
    try:
        user = User.objects.get(email=user_email)  # Find the user by email
    except User.DoesNotExist:
        return redirect('login')  # Redirect to login page if user is not found
    
    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.phone = request.POST.get('phone')
        user.blood_group = request.POST.get('blood_group') 
        user.address = request.POST.get('address')
        user.gender = request.POST.get('gender')
        user.date_of_birth = request.POST.get('date_of_birth')

        try:
            user.save()  # Save the updated user details
            messages.success(request, "Profile updated successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        
        return redirect('login') # Redirect to the user dashboard
    return render(request, 'update_profile.html', {'user': user})




def delete_account(request):
    # Retrieve the logged-in user's email from the session
    user_email = request.session.get('user_email')


    if not user_email:
        # If no user_email in session, redirect to login
        messages.error(request, "You need to log in to delete your account.")
        return redirect('login')

    try:
        # Find the user by email
        user = User.objects.get(email=user_email)
        user_appointment = appointment.objects.get(email = user_email)
    except User.DoesNotExist:
        # If the user doesn't exist, clear the session and redirect to login
        messages.error(request, "Account not found.")
        request.session.flush()
        return redirect('login')

    # Directly delete the user account
    user_appointment.delete()
    user.delete()
    request.session.flush()  # Clear session after account deletion
    messages.success(request, "Your account has been deleted successfully.")
    return redirect('login')  # Redirect to login after deletion


def logout(request):
    request.session.flush()  # Clears all session data
    return redirect('login')


def cancel_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        print("Appointment ID:", appointment_id)
        try:
            appointment_cancel = appointment.objects.get(id=appointment_id)
            print("Appointment found:", appointment_cancel)
            appointment_cancel.delete()
            messages.success(request, "Appointment cancelled successfully.")
        except appointment.DoesNotExist:
            messages.error(request, "Appointment not found.")
    return redirect('user_dashboard')  # Redirect to the user dashboard after cancellation
    




def doctor_dashboard(request):
    # Get session data manually
    user_email = request.session.get('user_email')
    user_name = request.session.get('user_name')
    user_type = request.session.get('user_type')
    is_authenticated = request.session.get('is_authenticated')
    user_phone = request.session.get('user_phone')
    blood_group = request.session.get('blood_group')
    date_of_birth = request.session.get('date_of_birth')
    gender = request.session.get('gender')
    address = request.session.get('address')
    specilization = request.session.get('specialization')


    # Check if the user is authenticated and is a doctor
    if  user_type != 'doctor':
        return HttpResponse("You are not authorized to view this page.", status=403)

    # Fetch appointments for the doctor
    current_date = datetime.now().date()
    upcoming_appointments = appointment.objects.filter(doctor_name=user_name, status='upcoming')
    past_appointments = appointment.objects.filter(doctor_name=user_name, status='completed')


    context = {
        'user_name': user_name,
        'user_email': user_email,
        'user_type': user_type,
        'user_phone': user_phone,
        'blood_group': blood_group,
        'dob': date_of_birth,
        'gender': gender,
        'address': address,
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'specialization': specilization,
    }

    return render(request, 'doctor_dashboard.html', context)





def prescription(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')

        try:
            # Fetch the appointment object
            appointment_obj = appointment.objects.get(id=appointment_id)
            user = User.objects.get(email=appointment_obj.email)  # Assumes email maps to user
        except appointment.DoesNotExist:
            messages.error(request, "Appointment not found.")
            return redirect('doctor_dashboard')
        except User.DoesNotExist:
            messages.error(request, "Patient associated with the appointment not found.")
            return redirect('doctor_dashboard')

        # Prepare the context with patient details
        content = {
            'name': appointment_obj.patient_name,
            'symptoms': appointment_obj.Symptoms,
            'date_of_birth': user.date_of_birth,
            'gender': user.gender,
            'appointment_id': appointment_id
        }
        return render(request, 'prescription.html', content)

    # Default redirect for GET request
    messages.error(request, "Invalid access method.")
    return redirect('doctor_dashboard')





def store_prescription(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        symptoms = request.POST.get('symptoms')
        diagnosis = request.POST.get('diagnosis')
        additional_instructions = request.POST.get('instructions')
        tests_to_conduct = request.POST.get('tests')
        follow_up_date = request.POST.get('follow_up')

        medicine_names = request.POST.getlist('medicine_name[]')
        dosages = request.POST.getlist('dosage[]')
        frequencies = request.POST.getlist('frequency[]')
        durations = request.POST.getlist('duration[]')

        try:
            # Fetch the appointment object and user (patient) data
            appointment_obj = appointment.objects.get(id=appointment_id)
            user = User.objects.get(email=appointment_obj.email)  # Assumes email maps to user

            doctor = request.session.get('user_name')
            patient = appointment_obj.patient_name
            symptoms = appointment_obj.Symptoms

            # Create the Prescription object
            prescription = Prescription.objects.create(
                doctor=doctor,
                patient_name=patient,
                patient_dob=user.date_of_birth,
                patient_gender=user.gender,
                symptoms=symptoms,
                diagnosis=diagnosis,
                additional_instructions=additional_instructions,
                tests_to_conduct=tests_to_conduct,
                follow_up_date=follow_up_date,
            )

            # Prepare medicines list
            medicines = []
            for name, dosage, frequency, duration in zip(medicine_names, dosages, frequencies, durations):
                medicines.append({
                    "medicine_name": name,
                    "dosage": dosage,
                    "frequency": frequency,
                    "duration": duration,
                })

            # Save medicines in the JSON field
            prescription.medicines = medicines
            prescription.status = 'complected'
            prescription.save()

            # Update appointment status
            appointment_obj.status = 'completed'  # Update the appointment status
            appointment_obj.save()  # Save the updated appointment

            messages.success(request, "Prescription stored successfully.")
            return redirect('doctor_dashboard')  # Redirect to the dashboard

        except User.DoesNotExist:
            messages.error(request, "Doctor or patient not found.")
            return redirect('prescription')  # Redirect back to prescription form if error occurs

    messages.error(request, "Invalid access method.")
    return redirect('doctor_dashboard')





from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.exceptions import ObjectDoesNotExist


def download_prescription(request):
    if request.method == 'POST':
        # Fetch appointment and prescription details
        appointment_id = request.POST.get('appointment_id')

        try:
            # Fetch the appointment object using the provided appointment_id
            appointment_obj = appointment.objects.get(id=appointment_id)
        except ObjectDoesNotExist:
            return HttpResponse("Appointment not found.", status=404)

        try:
            # Fetch the prescription object using the patient's name from the appointment
            prescription_obj = Prescription.objects.get(patient_name=appointment_obj.patient_name)
        except ObjectDoesNotExist:
            return HttpResponse("Prescription not found for the patient.", status=404)

        # Prepare context for rendering the HTML template
        context = {
            'prescription_obj': prescription_obj,
        }

        # Render the HTML content using the context
        html_content = render_to_string('prescription_template.html', context)

        # Convert HTML to PDF using WeasyPrint
        try:
            # Create a PDF from the HTML content
            pdf_file = HTML(string=html_content).write_pdf()
        except Exception as e:
            return HttpResponse(f"Error in generating PDF: {str(e)}", status=500)

        # Return the PDF as a response
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=Prescription_{prescription_obj.patient_name}.pdf'

        return response

    return HttpResponse("Invalid request", status=400)
