
from django.urls import path
from . import views
from .api import DirectoryAPI



urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard/<str:dir>', views.dashboard_view, name="dashboard"),
    path('edit/<str:dir>', views.edit_view, name="edit"),
    path('api/<int:dir>', DirectoryAPI.as_view(), name="directory_api"),
]
