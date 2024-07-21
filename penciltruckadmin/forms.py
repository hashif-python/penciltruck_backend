# forms.py

from django import forms
from .models import Gallery,Volunteer

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['title', 'description', 'image1', 'image2', 'image3', 'image4']


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['name', 'role', 'bio', 'image', 'email', 'phone']