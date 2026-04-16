# File: views.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 4/16/2026
# Description: The views file for the story planning app
# Creating the views for the story planning app

from django.shortcuts import render

# Create your views here.
def home(request):
    '''
    Creating a default view to handle the 'home' request.
    '''
    template_name = 'storyplanning/home.html'
    return render(request, template_name)