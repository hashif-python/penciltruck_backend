from django.urls import path, include
from . import views




urlpatterns = [
    path('login/', views.login,name='adminlogin'),
    path('', views.dashboard,name='admindashboard'),
    path('gallery', views.gallery,name='admingallery'),
    path('add_new_gallery/', views.add_new_gallery, name='add_new_gallery'),
    path('edit_gallery/', views.edit_gallery, name='edit_gallery'),
    path('delete_gallery/', views.delete_gallery, name='delete_gallery'),
    
    
]