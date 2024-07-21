from django.urls import path, include
from . import views




urlpatterns = [
    path('login/', views.login,name='adminlogin'),
    path('', views.dashboard,name='admindashboard'),
    path('gallery', views.gallery,name='admingallery'),
    path('add_new_gallery/', views.add_new_gallery, name='add_new_gallery'),
    path('edit_gallery/', views.edit_gallery, name='edit_gallery'),
    path('delete_gallery/', views.delete_gallery, name='delete_gallery'),
    path('volunteer-requests/', views.volunteer_requests, name='volunteer_requests'),
    path('update-volunteer-request-status/<int:pk>/', views.update_volunteer_request_status, name='update_volunteer_request_status'),
    path('volunteers/', views.volunteers, name='volunteers'),
    path('edit-volunteer/<int:pk>/', views.edit_volunteer, name='edit_volunteer'),
    
    
]