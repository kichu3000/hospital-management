from django.shortcuts import render, redirect
from home.models import User, appointment  # Ensure correct import of Appointment model
from home.views import get_doctors
from django.core.exceptions import ValidationError

# Create your views here.

def get_patient(request):
    patients = User.objects.filter(user_type='patient')
    return patients




def admin_dashboard(request):

    recent_patients = User.objects.filter(user_type='patient').order_by('-created_at')[:5]  # Get the latest 5 patients
    doctors = User.objects.filter(user_type='doctor').order_by('-created_at')[:5]  # Get the latest 5 doctors
    appointments = appointment.objects.all()  # Get all appointments

    patients = get_patient(request)
    content = {
        'patient_count' : patients.count(),
        'doctor_count' : get_doctors().count(),
        'total_users' : User.objects.all().count() - 1, # -1 to exclude the admin user
        'recent_patients' : recent_patients,
        'doctors' : doctors,
        'appoinments' : appointments
    }
    # print(appointments)
    return render(request,'admin/dashboard.html',content)




def patient_add(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            phone = request.POST['phone']
            user_type = request.POST['user_type']
            password2 = request.POST['confirm_password']
            blood_group = request.POST['blood_group']

            if password != password2:
                raise ValidationError("Passwords do not match")

            User.objects.create(
                name=name,
                email=email,
                password=password,
                phone=phone,
                user_type=user_type,
                blood_group=blood_group,
            )
            return redirect('my_admin:admin_dashboard')

        except KeyError as e:
            print(f"Missing POST parameter: {e}")
        except ValidationError as e:
            print(f"Validation error: {e}")

    return render(request, 'admin/patient_add.html')




def patient_list(request):
    patients = get_patient(request)
    return render(request,'admin/patients_list.html',{'patients':patients})