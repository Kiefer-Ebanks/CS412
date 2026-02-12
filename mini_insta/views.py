from django.shortcuts import render

from django.views.generic import ListView # Importing the ListView class
from .models import Profile # Importing the Profile model from the models.py file
# Create your views here.


class ProfileListView(ListView):
    ''' A view to display a list of all profiles '''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'