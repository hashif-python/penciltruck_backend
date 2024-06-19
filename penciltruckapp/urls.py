from django.urls import path, include
from .views import *




urlpatterns = [
    path('gallery', GalleryData.as_view()),
    
    
    
]