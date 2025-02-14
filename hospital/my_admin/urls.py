from django.urls import path,include
from . import views

app_name = 'my_admin' # This is the namespace for the app

urlpatterns = [

        path('',views.admin_dashboard,name='admin_dashboard'),
]