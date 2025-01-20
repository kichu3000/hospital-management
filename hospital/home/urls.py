from django.urls import path
from . import views
urlpatterns = [
    #path('',views.home,name='home'),
    path('',views.book_appointment,name='book_appointment'),
    path('signup/',views.signup_view,name='signup'),
    path('login/',views.login_view,name='login'),
    path('doctors/',views.doctor,name='doctors'),
    path('user_dashboard/',views.user_dashboard,name='user_dashboard'),
]
