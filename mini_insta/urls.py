# File: urls.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 2/12/2026
# Description: The urls file for the mini instagram app
# Creating the url pathsfor the mini instagram app

from django.urls import path
from .views import * #ProfileListView, ProfileDetailView, PostDetailView

# Creating the url paths for the mini instagram app
urlpatterns = [
    path(r'', ProfileListView.as_view(), name='show_all_profiles'),
    path(r'profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    path(r'post/<int:pk>/', PostDetailView.as_view(), name='show_post'),
    path(r'profile/<int:pk>/create_post/', CreatePostView.as_view(), name='create_post'),
    path(r'profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile'),
]