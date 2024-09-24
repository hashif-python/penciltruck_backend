from django.urls import path, include
from .views import *




urlpatterns = [
    path('gallery', GalleryData.as_view()),
    path('volunteer-request', VolunteerRequestCreate.as_view()),
    path('send-otp/', VerifyOtpView.as_view(), name='send-otp'),
    path('study-material-donations/', StudyMaterialDonationListCreate.as_view(), name='study-material-donations-list-create'),

    
    
    
]