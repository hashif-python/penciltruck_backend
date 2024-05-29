from django.shortcuts import  redirect,render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .decorators import *
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
def banners(request):
	return render(request,'penciltruckadmin/banners.html')