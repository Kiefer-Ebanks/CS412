# File: urls.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 2/12/2026
# Description: The urls file for the mini instagram app
# Creating the url pathsfor the mini instagram app


from django.urls import path
from .views import ProfileListView

urlpatterns = [
    path(r'', ProfileListView.as_view(), name='show_all_profiles'),
]