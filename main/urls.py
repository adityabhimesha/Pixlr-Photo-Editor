
from django.urls import path
from . import views
from .api import DirectoryAPI, EditAPI



urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard/<str:dir>', views.dashboard_view, name="dashboard"),
    path('edit/<str:dir>', views.edit_view, name="edit"),
    path('api/<int:dir>', DirectoryAPI.as_view(), name="directory_api"),
    path('edit/api/<int:dir>', EditAPI.as_view(), name="edit_api"),
]
