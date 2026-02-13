from django.shortcuts import render

from django.views.generic import ListView, DetailView # Importing the ListView and DetailView classes
from .models import Profile # Importing the Profile model from the models.py file
# Create your views here.


class ProfileListView(ListView):
    ''' A view to display a list of all profiles '''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles' # using plural variable name for the profiles list


class ProfileDetailView(DetailView):
    ''' A view to display a single profile '''

    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile' # using singular variable name for the profile object