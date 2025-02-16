from django.urls import path,include
from . import views

app_name = 'my_admin' # This is the namespace for the app

urlpatterns = [
        path('',views.admin_dashboard,name='admin_dashboard'),
        path('patient_add/',views.patient_add,name='patient_add'),
        path('patient_list/',views.patient_list,name='patient_list'),
]