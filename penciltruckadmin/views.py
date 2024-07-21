import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from .decorators import *
from . models import *
from .forms import GalleryForm, VolunteerForm
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
                gallery.image1 = None # type: ignore
            if request.POST.get('delete_image2') == 'true':
                gallery.image2.delete(save=False)
                gallery.image2 = None # type: ignore
            if request.POST.get('delete_image3') == 'true':
                gallery.image3.delete(save=False)
                gallery.image3 = None # type: ignore
            if request.POST.get('delete_image4') == 'true':
                gallery.image4.delete(save=False)
                gallery.image4 = None # type: ignore

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




def volunteer_requests(request):
    requests = VolunteerRequest.objects.all()
    return render(request, 'penciltruckadmin/volunteer_requests.html', {'requests': requests})

def update_volunteer_request_status(request, pk):
    volunteer_request = get_object_or_404(VolunteerRequest, pk=pk)
    status = request.GET.get('status')
    
    if status == 'Accepted':
        # Insert details into Volunteer model
        Volunteer.objects.create(
            name=volunteer_request.name,
            role='Volunteer',  # Assuming role is fixed as 'Volunteer', change if needed
            email=volunteer_request.email,
            phone=volunteer_request.phone,
            bio=volunteer_request.message,  # Assuming the message field can be used as bio
        )
        volunteer_request.status = status
        volunteer_request.save()
        messages.success(request, 'Volunteer request has been accepted and details added.')
    elif status == 'Rejected':
        volunteer_request.status = status
        volunteer_request.save()
        messages.success(request, 'Volunteer request has been rejected.')
    else:
        messages.error(request, 'Invalid status.')

    return redirect('volunteer_requests')


def volunteers(request):
    volunteer_list = Volunteer.objects.all()
    return render(request, 'penciltruckadmin/volunteers.html', {'volunteers': volunteer_list})


def edit_volunteer(request, pk):
    volunteer = get_object_or_404(Volunteer, pk=pk)
    if request.method == "POST":
        form = VolunteerForm(request.POST, request.FILES, instance=volunteer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Volunteer details updated successfully!')
            return redirect('volunteers')
    else:
        form = VolunteerForm(instance=volunteer)
    return render(request, 'penciltruckadmin/edit_volunteer.html', {'form': form, 'volunteer': volunteer})



def logout_view(request):
    logout(request)
    return redirect('adminlogin')