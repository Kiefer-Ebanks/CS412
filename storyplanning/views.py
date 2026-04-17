# File: views.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 4/16/2026
# Description: The views file for the story planning app
# Creating the views for the story planning app

from django.shortcuts import render
from django.views.generic import ListView # importing the ListView for the ideas page
from .models import Idea # importing the Idea model for the ideas page

# Create your views here.
def home(request):
    '''
    Creating a default view to handle the 'home' request.
    '''
    template_name = 'storyplanning/home.html'
    return render(request, template_name)


class ShowAllIdeas(ListView):
    '''
    Creating a view to show all ideas
    '''

    model = Idea
    template_name = 'storyplanning/all_ideas.html'
    context_object_name = 'ideas'