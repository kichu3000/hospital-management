from django.urls import path
from . import views
urlpatterns = [
    #path('',views.home,name='home'),
    path('',views.book_appointment,name='book_appointment'),
    path('signup/',views.signup_view,name='signup'),
    path('login/',views.login_view,name='login'),
    path('dashboard/',views.dashboard,name='dashboard'),#not created yet
    
]
