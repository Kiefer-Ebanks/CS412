# File: urls.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 4/16/2026
# Description: The urls file for the story planning app
# Creating the url paths for the story planning app

from django.urls import path
from . import views

from django.contrib.auth import views as auth_views # importing the views for the authentication system

urlpatterns = [
    path(r'', views.home, name='home'), # URL pattern for the view to display the home page

    # Authentication URLs
    path(r'login/', auth_views.LoginView.as_view(template_name='storyplanning/login.html'), name='login'), # providing the template and login form via the auth_views.LoginView
    path(r'logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'), # providing the template and logout form via the auth_views.LogoutView
]