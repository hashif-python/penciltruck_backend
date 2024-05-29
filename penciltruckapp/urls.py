from django.urls import path, include
from .views import *




urlpatterns = [
    path('banners', Banners.as_view()),
    
    
]