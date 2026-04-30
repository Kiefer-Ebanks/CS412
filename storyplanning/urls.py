# File: urls.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 4/16/2026
# Description: The urls file for the story planning app
# Creating the url paths for the story planning app

from django.urls import path
from . import views
from .views import * # importing all the views from the views.py file
from django.contrib.auth import views as auth_views # importing the views for the authentication system

urlpatterns = [
    path(r'', auth_views.LoginView.as_view(template_name='storyplanning/login.html'), name='home'), # default URL pattern for the app which will take users to the login page
    
    # URL patterns for the idea views
    path(r'ideas/', ShowAllIdeas.as_view(), name='show_all_ideas'), # URL pattern for the view to show all ideas
    path(r'idea/create/', CreateIdeaView.as_view(), name='create_idea'), # URL pattern for the view to create an idea
    path(r'idea/<int:pk>/', IdeaView.as_view(), name='idea'), # URL pattern for the view to show an idea

    # URL patterns for the scene views
    path(r'idea/<int:idea_pk>/scene/<int:scene_pk>/', SceneView.as_view(), name='scene'), # URL pattern for the view to show a scene
    path(r'scene/<int:scene_pk>/', SceneView.as_view(), name='scene_only'), # another URL pattern for the same view that shows a scene (got the idea from speaking to Professor Stevens)
    path(r'idea/<int:idea_pk>/create_scene/', CreateSceneView.as_view(), name='create_scene'), # URL pattern for the view to create a scene for an idea

    # URL patterns for the character views
    path(r'idea/<int:idea_pk>/character/<int:character_pk>/', CharacterView.as_view(), name='character'), # URL pattern for the view to show a character
    path(r'idea/<int:idea_pk>/create_character/', CreateCharacterView.as_view(), name='create_character'), # URL pattern for the view to create a character for an idea
    path(r'idea/<int:idea_pk>/scene/<int:scene_pk>/character/<int:character_pk>/', CharacterView.as_view(), name='character_for_scene'), # URL pattern for the view to see a character related to a specific scene
    path(r'idea/<int:idea_pk>/scene/<int:scene_pk>/create_character/', CreateCharacterView.as_view(), name='create_character_for_scene'), # URL pattern for the view to create a character for a specific scene
    
    # URL patterns for the image views
    path(r'idea/<int:idea_pk>/image/<int:image_pk>/', ImageView.as_view(), name='image'), # URL pattern for the view to show an image from an idea
    path(r'idea/<int:idea_pk>/create_image/', CreateImageView.as_view(), name='create_image'), # URL pattern for the view to create an image for an idea
    path(r'idea/<int:idea_pk>/scene/<int:scene_pk>/image/<int:image_pk>/', ImageView.as_view(), name='image_for_scene'), # URL pattern for the view to show an image related to a specific scene
    path(r'idea/<int:idea_pk>/scene/<int:scene_pk>/create_image/', CreateImageView.as_view(), name='create_image_for_scene'), # URL pattern for the view to create an image for a specific scene
    path(r'idea/<int:idea_pk>/character/<int:character_pk>/image/<int:image_pk>/', ImageView.as_view(), name='image_for_character'), # URL pattern for the view to show an image related to a specific character
    path(r'idea/<int:idea_pk>/character/<int:character_pk>/create_image/', CreateImageView.as_view(), name='create_image_for_character'), # URL pattern for the view to create an image for a specific character
    
    # Authentication URLs
    path(r'login/', auth_views.LoginView.as_view(template_name='storyplanning/login.html'), name='login'), # providing the template and login form via the auth_views.LoginView
    path(r'logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), # providing the template and logout form via the auth_views.LogoutView
    path(r'register/', UserRegistrationView.as_view(), name='register'), # providing the template and register form via the RegistrationView

    # Authentication API Views:
    path(r'api/login/', UserLoginAPIView.as_view(), name='api_login'),
    path(r'api/register/', UserRegistrationAPIView.as_view(), name='api_register'),

    # StoryPlanning API Views:
    path(r'api/ideas/', IdeaListAPIView.as_view(), name='api_ideas'),
    path(r'api/ideas/<int:pk>/', IdeaDetailAPIView.as_view(), name='api_idea'),
    path(r'api/scenes/<int:pk>/', SceneDetailAPIView.as_view(), name='api_scene'),
]