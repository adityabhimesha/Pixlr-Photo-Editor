from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from main.models import Directory

@login_required(login_url='/auth/login/')
def logout_request(request):
    logout(request)
    return render(request, "logout.html", {"title" : "Logout"})

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			if user is not None:
				login(request, user)
				home_dir = Directory(user_id=request.user, directory_name='home')
				try:
					home_dir.save()
				except:
					messages.error(request, "There Has Been A Problem, Please Try Again.")
					return redirect('/')
				messages.success(request, "Registration successful." )
				return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form, "title":"Register"})



def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, "Login successful." )
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.warning(request,"Please Try Again!")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form, "title":"Login"})