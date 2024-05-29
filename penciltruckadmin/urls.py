from django.urls import path, include
from . import views




urlpatterns = [
    path('login/', views.login,name='adminlogin'),
    path('', views.dashboard,name='admindashboard'),
    path('banners', views.banners,name='adminbanners'),
    
    
]