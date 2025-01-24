from django.urls import path
from . import views
urlpatterns = [
    path('',views.book_appointment,name='book_appointment'),
    path('signup/',views.signup_view,name='signup'),
    path('login/',views.login_view,name='login'),
    path('doctors/',views.doctor,name='doctors'),
    path('user_dashboard/',views.user_dashboard,name='user_dashboard'),
    path('update_profile/',views.update_profile,name='update_profile'),
    path('delete_account/',views.delete_account,name='delete_account'),
    path('logout/',views.logout,name='logout'),
    path('cancel_appointment/',views.cancel_appointment,name='cancel_appointment'),
    path('doctor_dashboard/',views.doctor_dashboard,name='doctor_dashboard'),
    path('prescription/',views.prescription,name='prescription'),
]
