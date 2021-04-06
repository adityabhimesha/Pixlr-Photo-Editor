from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Directory
from .forms import *
from django.contrib import messages


def home(request):

    if request.user.is_authenticated:
        home_dir = Directory.objects.filter(user_id=request.user, directory_name="home")
        print(home_dir)
        home_dir = home_dir[0].pk
    else:
        home_dir = -1
    return render(request, template_name="home.html", context={"title" : "Home","home_dir" : home_dir})


@login_required(login_url='/auth/login/')
def dashboard_view(request, dir):
    
    parent_dir = Directory.objects.get(pk=dir)
    dirs = Directory.objects.filter(user_id_id=request.user, parent_directory=parent_dir)
    if len(dirs) == 0:
        dirs = None

    context = {
        "title" : "Dashboard",
        "home_dir" : parent_dir,
        "dirs" : dirs,
    }
    return render(request, template_name="dashboard.html", context=context)


@login_required(login_url='/auth/login/')
def edit_view(request, dir):
    
    try:
        image = Directory.objects.get(pk=dir)
    except Directory.DoesNotExist:
        image = None

    context = {
        "title" : "Edit Image",
        "image" : image,
    }
    return render(request, template_name="dashboard.html", context=context)




