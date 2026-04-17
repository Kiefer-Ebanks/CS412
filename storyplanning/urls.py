# File: urls.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 4/16/2026
# Description: The urls file for the story planning app
# Creating the url paths for the story planning app

from django.urls import path
from . import views

from django.contrib.auth import views as auth_views # importing the views for the authentication system
from .views import ShowAllIdeas # importing the view to show all ideas

urlpatterns = [
    path(r'', auth_views.LoginView.as_view(template_name='storyplanning/login.html'), name='home'), # default URL pattern for the app which will take user's to the login page
    path(r'ideas/', ShowAllIdeas.as_view(), name='show_all_ideas'), # URL pattern for the view to show all ideas

    # Authentication URLs
    path(r'login/', auth_views.LoginView.as_view(template_name='storyplanning/login.html'), name='login'), # providing the template and login form via the auth_views.LoginView
    path(r'logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), # providing the template and logout form via the auth_views.LogoutView
]