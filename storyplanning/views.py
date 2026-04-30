# File: views.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 4/16/2026
# Description: The views file for the story planning app
# Creating the views for the story planning app

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView # importing the ListView, CreateView, and DetailView for the ideas page
from .models import Idea, Scene, Character, Image # models for the story planning app
from .forms import * # importing the CreateIdeaForm, CreateSceneForm, and CreateCharacterForm for the ideas, scenes, and characters pages
from .serializers import *
from django.contrib.auth.mixins import LoginRequiredMixin # importing the LoginRequiredMixin for authentication
from django.urls import reverse # importing the reverse function
from django.contrib.auth.forms import UserCreationForm # importing the UserCreationForm for creating a new user
from django.contrib.auth.models import User # importing the User model for creating a new user
from django.contrib.auth import authenticate, login # importing auth functions to authenticate a user and login a user

# REST API auth imports
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


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

class ImageView(LoginRequiredMixin, DetailView):
    ''' Creating a view to show an image '''

    model = Image
    template_name = 'storyplanning/image.html'
    context_object_name = 'image'
    pk_url_kwarg = 'image_pk'  # Telling DetailView to use image_pk instead of pk

    def get_login_url(self):
        ''' Redirect the user to the login page if the user is not logged in '''
        return reverse('login')

    def get_queryset(self):
        ''' Return the queryset of images that belong to the logged-in user across all ideas, scenes, and characters '''
        idea_pk = self.kwargs['idea_pk']

        if 'character_pk' in self.kwargs:
            return Image.objects.filter(idea=idea_pk, character=self.kwargs['character_pk'])
            
        if 'scene_pk' in self.kwargs:
            scene = get_object_or_404(Scene, pk=self.kwargs['scene_pk'], idea=idea_pk) # ensuring the scene belongs to the idea and the scene actually exists
            return scene.get_all_images()

        return Image.objects.filter(idea=idea_pk)


class CreateImageView(LoginRequiredMixin, CreateView):
    ''' Creating a view to create an image '''

    form_class = CreateImageForm
    template_name = 'storyplanning/create_image_form.html'
    context_object_name = 'image'

    def get_login_url(self):
        ''' Redirect the user to the login page if the user is not logged in '''
        return reverse('login')

    def form_valid(self, form):
        ''' Add the idea and scene objects to the image and save it '''

        idea = Idea.objects.get(pk=self.kwargs['idea_pk']) # adding the foreign key of the idea to the image object before saving it to the database
        scene = None
        character = None

        if 'scene_pk' in self.kwargs:
            scene = Scene.objects.get(pk=self.kwargs['scene_pk']) # adding the foreign key of the scene to the image object before saving it to the database

        if 'character_pk' in self.kwargs:
            character = Character.objects.get(pk=self.kwargs['character_pk']) # adding the foreign key of the character to the image object before saving it to the database

        image_url = self.request.POST.get('image_url')
        description = self.request.POST.get('description')
        files = self.request.FILES.getlist('files') # Read the image files from self.request.FILES

        # Require either a URL or at least one uploaded file
        if not image_url and not files:
            form.add_error('image_url', 'Add an image URL or upload at least one image')
            return self.form_invalid(form)

        created_images = []
        for file in files:
            created_images.append(Image.objects.create( # create a new Image object for each file with the saved idea, scene, character, and description
                idea=idea,
                scene=scene,
                character=character,
                image_file=file,
                description=description,
            ))

        # this is the url only path if the user only provides a URL and no files
        if not created_images:
            created_images.append(Image.objects.create( # create a new Image object with the saved idea, scene, character, image_url, and description
                idea=idea,
                scene=scene,
                character=character,
                image_url=image_url,
                description=description,
            ))

        self.object = created_images[0] # set the self.object to the first created image
        return HttpResponseRedirect(self.get_success_url()) # redirect the user to the success url

    def get_success_url(self):
        ''' Redirect the user to the image page after creating an image '''

        if 'scene_pk' in self.kwargs:
            return reverse('image_for_scene', kwargs={'idea_pk': self.kwargs['idea_pk'], 'scene_pk': self.kwargs['scene_pk'], 'image_pk': self.object.pk})
        elif 'character_pk' in self.kwargs:
            return reverse('image_for_character', kwargs={'idea_pk': self.kwargs['idea_pk'], 'character_pk': self.kwargs['character_pk'], 'image_pk': self.object.pk})
        else:
            return reverse('image', kwargs={'idea_pk': self.kwargs['idea_pk'], 'image_pk': self.object.pk})


    def get_context_data(self, **kwargs):
        ''' Add the idea object to the context so the template can show the idea title '''

        context = super().get_context_data(**kwargs)
        context['idea'] = Idea.objects.get(pk=self.kwargs['idea_pk'])

        if 'scene_pk' in self.kwargs:
            context['scene'] = Scene.objects.get(pk=self.kwargs['scene_pk'])

        if 'character_pk' in self.kwargs:
            context['character'] = Character.objects.get(pk=self.kwargs['character_pk'])

        return context


#  API Authentication Views

class UserLoginAPIView(APIView):
    ''' API view to login a user '''

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        ''' logins in a user and returns DRF token for React'''

        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
            },
            status = status.HTTP_200_OK # returning a 200 OK status code to indicate that the user was successfully logged in
        )


class UserRegistrationAPIView(APIView):
    ''' API view to register a new user '''

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        ''' register a new user and return token '''
        serializer = UserSerializer(data=request.data) # creating a new UserSerializer object with the data from the request
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
            },
            status = status.HTTP_201_CREATED # returning a 201 Created status code to indicate that the user was successfully registered
        )


class ChangePasswordAPIView(APIView):
    ''' API view to change a user's password '''

    permission_classes = [IsAuthenticated]

    def post(self, request):
        ''' changing a user's password '''

        serializer = ChangePasswordSerializer(data=request.data) # create a new ChangePasswordSerializer object with the data from the request
        serializer.is_valid(raise_exception=True)
        cur = serializer.validated_data['current_password'] # get the current password from the validated data
        new_pw = serializer.validated_data['new_password'] # get the new password from the validated data
        
        if not request.user.check_password(cur): # check if the current password is correct
            return Response(
                {'error': 'Current password is incorrect'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.set_password(new_pw)
        request.user.save()
        return Response({'detail': 'Password updated'}, status=status.HTTP_200_OK)


class ChangeUsernameAPIView(APIView):
    ''' API view to change a user's username '''

    permission_classes = [IsAuthenticated]

    def post(self, request):
        ''' change authenticated user's username '''

        serializer = ChangeUsernameSerializer(data=request.data) # validates the new username from request body
        serializer.is_valid(raise_exception=True)
        new_name = serializer.validated_data['new_username'].strip() # get the new username from the validated data and strip any whitespace

        if not new_name:
            return Response({'error': 'Username cannot be blank'}, status=status.HTTP_400_BAD_REQUEST)

        # keep usernames unique by checking if the new username already exists in the database
        if User.objects.filter(username=new_name).exclude(pk=request.user.pk).exists():
            return Response({'error': 'That username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.username = new_name # set the new username to the user's username
        request.user.save() # save the new username to the database
        
        return Response({'detail': 'Username updated', 'username': request.user.username}, status=status.HTTP_200_OK) # returning a 200 OK status code to indicate that the user's username was successfully updated


class DeleteAccountAPIView(APIView):
    ''' API view to delete a user's account '''

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        ''' deleting a user's account and all related data '''

        request.user.delete()  # this deletes the user from the database and cascades the delete to remove ideas, scenes, characters, images via FK on_delete rules

        return Response(status=status.HTTP_204_NO_CONTENT) # returning a 204 No Content status code to indicate that the user's account was successfully deleted


class IdeaListAPIView(generics.ListCreateAPIView):
    ''' API view to list/create ideas for the authenticated user '''

    serializer_class = IdeaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Idea.objects.filter(user=self.request.user)


class IdeaDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    ''' API view to retrieve/update/delete one of the authenticated user's ideas '''

    serializer_class = IdeaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Idea.objects.filter(user=self.request.user)


class SceneDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    ''' API view to get, update, or delete a scene '''

    serializer_class = SceneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ''' only get scenes that belong to the authenticated user'''

        return Scene.objects.filter(idea__user=self.request.user)


class CharacterDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    ''' API view to get, update, or delete a character '''

    serializer_class = CharacterSerializer
    permission_classes = [IsAuthenticated] # only allow authenticated users to access this view

    def get_queryset(self):
        ''' only get characters that belong to ideas owned by the user '''

        return Character.objects.filter(idea__user=self.request.user)


class ImageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ API view to get, update, or delete an image that belongs to one of the user's ideas """

    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ''' only get images for ideas owned by the user '''

        return Image.objects.filter(idea__user=self.request.user)