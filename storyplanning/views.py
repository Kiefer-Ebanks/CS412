# File: views.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 4/16/2026
# Description: The views file for the story planning app
# Creating the views for the story planning app

from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView # importing the ListView, CreateView, and DetailView for the ideas page
from .models import Idea, Scene, Character # importing the Idea, Scene, and Character models for the ideas, scenes, and characters pages
from .forms import * # importing the CreateIdeaForm, CreateSceneForm, and CreateCharacterForm for the ideas, scenes, and characters pages
from django.contrib.auth.mixins import LoginRequiredMixin # importing the LoginRequiredMixin for authentication
from django.urls import reverse # importing the reverse function
from django.contrib.auth.forms import UserCreationForm # importing the UserCreationForm for creating a new user
from django.contrib.auth.models import User # importing the User model for creating a new user
from django.contrib.auth import login # importing the login function for logging in a user right after they register


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

    def get_queryset(self):
        ''' Return the queryset of ideas that belong to the logged-in user '''
        return Idea.objects.filter(user=self.request.user)

class IdeaView(LoginRequiredMixin, DetailView):
    ''' Creating a view to show an idea '''

    model = Idea
    template_name = 'storyplanning/idea.html'
    context_object_name = 'idea'

    def get_login_url(self):
        ''' Redirect the user to the login page if the user is not logged in '''
        return reverse('login') # redirecting to the login page

    def get_queryset(self):
        ''' Return the queryset of ideas that belong to the logged-in user '''
        return Idea.objects.filter(user=self.request.user)
    
    def get_all_characters(self):
        ''' Return all characters that belong to the idea '''
        return Character.objects.filter(idea=self.get_object())

class CreateIdeaView(LoginRequiredMixin, CreateView):
    '''
    Creating a view to create an idea
    '''

    form_class = CreateIdeaForm
    template_name = 'storyplanning/create_idea_form.html'
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

    def get_success_url(self):
        ''' The page to redirect the user to after successful registration '''
        return reverse('show_all_ideas') # redirecting to the show_all_ideas page

    def form_valid(self, form):
        ''' Automatically logging the user in after successful registration '''

        response = super().form_valid(form) # calling the form_valid method to save the new user object and build the redirect to get_success_url()
        login(self.request, self.object) # logging in the user with the new userobject that was created
        return response 

class SceneView(LoginRequiredMixin, DetailView):
    ''' Creating a view to show a scene '''

    model = Scene
    template_name = 'storyplanning/scene.html'
    context_object_name = 'scene'
    pk_url_kwarg = 'scene_pk'  # Tell DetailView to use scene_pk instead of pk

    def get_login_url(self):
        ''' Redirect the user to the login page if the user is not logged in '''
        return reverse('login')

    def get_queryset(self):
        ''' Return the queryset of scenes that belong to the logged-in user '''
        return Scene.objects.filter(idea=self.kwargs['idea_pk'])

class CreateSceneView(LoginRequiredMixin, CreateView):
    ''' Creating a view to create a scene '''

    form_class = CreateSceneForm
    template_name = 'storyplanning/create_scene_form.html'
    context_object_name = 'scene'

    def get_login_url(self):
        ''' Redirect the user to the login page if the user is not logged in '''
        return reverse('login')
    
    def get_context_data(self, **kwargs):
        ''' Add the idea object to the context so the template can show the idea title '''

        context = super().get_context_data(**kwargs)
        context['idea'] = Idea.objects.get(pk=self.kwargs['idea_pk'])
        return context

    def form_valid(self, form):
        ''' Add the idea object to the scene and save it '''

        form.instance.idea = Idea.objects.get(pk=self.kwargs['idea_pk']) # adding the foreign key of the idea to the scene object before saving it to the database
        return super().form_valid(form)

    def get_success_url(self):
        ''' Redirect the user to the idea page after creating a scene '''

        # using the idea_pk from the URL pattern and the scene_pk of the scene that was just created to redirect the user to the scene page of the newly created scene
        return reverse('scene', kwargs={'idea_pk': self.kwargs['idea_pk'], 'scene_pk': self.object.pk})
    
class CharacterView(LoginRequiredMixin, DetailView):
    ''' Creating a view to show a character '''

    model = Character
    template_name = 'storyplanning/character.html'
    context_object_name = 'character'
    pk_url_kwarg = 'character_pk'  # Telling DetailView to use character_pk instead of pk

    def get_login_url(self):
        ''' Redirect the user to the login page if the user is not logged in '''

        return reverse('login')

    def get_queryset(self):
        ''' Return the queryset of characters that belong to the logged-in user '''

        return Character.objects.filter(idea=self.kwargs['idea_pk'])


class CreateCharacterView(LoginRequiredMixin, CreateView):
    ''' Creating a view to create a character '''

    form_class = CreateCharacterForm
    template_name = 'storyplanning/create_character_form.html'
    context_object_name = 'character'
    
    def get_login_url(self):
        ''' Redirect the user to the login page if the user is not logged in '''
        return reverse('login')

    def form_valid(self, form):
        ''' Adding the idea and scene objects to the character and save it '''

        form.instance.idea = Idea.objects.get(pk=self.kwargs['idea_pk']) # adding the foreign key of the idea to the character object before saving it to the database

        if 'scene_pk' in self.kwargs:
            form.instance.scene = Scene.objects.get(pk=self.kwargs['scene_pk']) # adding the foreign key of the scene to the character object before saving it to the database

        return super().form_valid(form)

    def get_success_url(self):
        ''' Redirect the user to the idea page after creating a scene '''

        if 'scene_pk' in self.kwargs:
            # redirecting to the character_for_scene page if a scene_pk is provided
            return reverse('character_for_scene', kwargs={'idea_pk': self.kwargs['idea_pk'], 'scene_pk': self.kwargs['scene_pk'], 'character_pk': self.object.pk})
        else:
            # redirecting to the character page if no scene_pk is provided
            return reverse('character', kwargs={'idea_pk': self.kwargs['idea_pk'], 'character_pk': self.object.pk})

    def get_context_data(self, **kwargs):
        ''' Add the idea object to the context so the template can show the idea title '''

        context = super().get_context_data(**kwargs)
        context['idea'] = Idea.objects.get(pk=self.kwargs['idea_pk'])

        if 'scene_pk' in self.kwargs:
            context['scene'] = Scene.objects.get(pk=self.kwargs['scene_pk'])
        return context

