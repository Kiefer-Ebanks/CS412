# File: views.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 4/16/2026
# Description: The views file for the story planning app
# Creating the views for the story planning app

from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView # importing the ListView, CreateView, and DetailView for the ideas page
from .models import Idea # importing the Idea model for the ideas page
from .forms import CreateIdeaForm # importing the CreateIdeaForm for the ideas page
from django.contrib.auth.mixins import LoginRequiredMixin # importing the LoginRequiredMixin for authentication
from django.urls import reverse # importing the reverse function
from django.contrib.auth.forms import UserCreationForm # importing the UserCreationForm for creating a new user
from django.contrib.auth.models import User # importing the User model for creating a new user


class ShowAllIdeas(LoginRequiredMixin, ListView):
    '''
    Creating a view to show all ideas
    '''

    model = Idea
    template_name = 'storyplanning/all_ideas.html'
    context_object_name = 'ideas'

    def get_login_url(self):
        ''' Redirect the user to the login page if the user is not logged in '''
        return reverse('login') # redirecting to the login page

class IdeaView(LoginRequiredMixin, DetailView):
    ''' Creating a view to show an idea '''

    model = Idea
    template_name = 'storyplanning/idea.html'
    context_object_name = 'idea'

    def get_login_url(self):
        ''' Redirect the user to the login page if the user is not logged in '''
        return reverse('login') # redirecting to the login page

class CreateIdeaView(LoginRequiredMixin, CreateView):
    '''
    Creating a view to create an idea
    '''

    form_class = CreateIdeaForm
    template_name = 'storyplanning/create_idea.html'
    context_object_name = 'idea'

    def get_login_url(self):
        ''' Redirect the user to the login page if the user is not logged in '''
        return reverse('login') # redirecting to the login page

    def form_valid(self, form):
        ''' Add the user to the idea and save it '''
        form.instance.user = self.request.user
        return super().form_valid(form)

class UserRegistrationView(CreateView):
    ''' Creating a view to show and process the form for creating a new user '''

    model = User
    form_class = UserCreationForm
    template_name = 'storyplanning/register.html'
    context_object_name = 'user'

    def get_login_url(self):
        ''' Redirect the user to the login page if the user is not logged in '''
        return reverse('login') # redirecting to the login page

    def get_success_url(self):
        ''' The page to redirect the user to after successful registration '''
        return reverse('login') # redirecting to the login page