from multiprocessing import context
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .decorators import *
from . models import *
from .forms import GalleryForm
from django.urls import reverse  # Import reverse here


# Create your views here.



def login(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			if user.is_superuser:
				auth_login(request, user)
				return redirect('admindashboard')  # Redirect to the admin home page
			else:
				messages.error(request, "You do not have superuser privileges.")
		else:
			messages.error(request, "Invalid username or password.")
	return render(request,'penciltruckadmin/login.html')

@user_passes_test(is_superadmin)
def dashboard(request):
	return render(request,'penciltruckadmin/dashboard.html')

@user_passes_test(is_superadmin)
def gallery(request):
	gallery_data=Gallery.objects.all()
	context={'gallery_data':gallery_data}
 
	return render(request,'penciltruckadmin/gallery.html',context)


def add_new_gallery(request):
    if request.method == "POST":
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('admingallery'))
    else:
        form = GalleryForm()
    return render(request, 'penciltruckadmin/gallery.html', {'form': form})



def edit_gallery(request):
    id=request.POST.get('id')
    gallery = get_object_or_404(Gallery, id=id)
    if request.method == "POST":
        form = GalleryForm(request.POST, request.FILES, instance=gallery)
        if form.is_valid():
            if request.POST.get('delete_image1') == 'true':
                gallery.image1.delete(save=False)
                gallery.image1 = None
            if request.POST.get('delete_image2') == 'true':
                gallery.image2.delete(save=False)
                gallery.image2 = None
            if request.POST.get('delete_image3') == 'true':
                gallery.image3.delete(save=False)
                gallery.image3 = None
            if request.POST.get('delete_image4') == 'true':
                gallery.image4.delete(save=False)
                gallery.image4 = None

            form.save()
            messages.success(request, 'Gallery image updated successfully!')
            return redirect(reverse('admingallery'))
    else:
        form = GalleryForm(instance=gallery)
    return render(request, 'penciltruckadmin/gallery.html', {'form': form, 'edit': True, 'gallery': gallery})

def delete_gallery(request):
    id=request.POST.get('id')
    gallery = get_object_or_404(Gallery, id=id)
    if request.method == "POST":
        gallery.delete()
        messages.success(request, 'Gallery image deleted successfully!')
        return redirect(reverse('admingallery'))
    return render(request, 'penciltruckadmin/gallery.html', {'gallery': gallery})