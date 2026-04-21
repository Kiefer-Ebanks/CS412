# File: urls.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 4/16/2026
# Description: The urls file for the story planning app
# Creating the url paths for the story planning app

from django.urls import path
from . import views
from .views import * # importing all the views from the views.py file
from django.contrib.auth import views as auth_views # importing the views for the authentication system

urlpatterns = [
    path(r'', auth_views.LoginView.as_view(template_name='storyplanning/login.html'), name='home'), # default URL pattern for the app which will take user's to the login page
    
    # URL patterns for the idea views
    path(r'ideas/', ShowAllIdeas.as_view(), name='show_all_ideas'), # URL pattern for the view to show all ideas
    path(r'idea/create/', CreateIdeaView.as_view(), name='create_idea'), # URL pattern for the view to create an idea
    path(r'idea/<int:pk>/', IdeaView.as_view(), name='idea'), # URL pattern for the view to show an idea
    path(r'idea/<int:idea_pk>/scene/<int:scene_pk>/', SceneView.as_view(), name='scene'), # URL pattern for the view to show a scene
    path(r'scene/<int:scene_pk>/', SceneView.as_view(), name='scene_only'), # another URL pattern for the same view that shows a scene (got the idea from speaking to Professor Stevens)

    # Authentication URLs
    path(r'login/', auth_views.LoginView.as_view(template_name='storyplanning/login.html'), name='login'), # providing the template and login form via the auth_views.LoginView
    path(r'logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), # providing the template and logout form via the auth_views.LogoutView
    path(r'register/', UserRegistrationView.as_view(), name='register'), # providing the template and register form via the RegistrationView
]