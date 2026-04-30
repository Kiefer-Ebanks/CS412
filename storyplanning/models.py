# File: models.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 4/16/2026
# Description: The models file for the story planning app
# Creating the models for the story planning app

from django.db import models
from django.contrib.auth.models import User # importing the User model
from django.urls import reverse # importing the reverse function

class Idea(models.Model):
    ''' models the data attributes of an idea '''

    title = models.TextField()
    storyboard = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # adding to the Idea model to link it to the User model

    def __str__(self):
        ''' returns a string representation of the Idea model that is just the title '''
        return f'{self.title}'

    def get_absolute_url(self):
        ''' returns the absolute url for the Idea model so when a new idea is created, it will redirect to the idea page '''
        
        return reverse('idea', kwargs={'pk': self.pk})

    def get_all_scenes(self):
        ''' returns all scenes related to an idea by Foreign Key'''

        return Scene.objects.filter(idea=self)

    def get_all_characters(self):
        ''' returns all characters for an idea '''

        return Character.objects.filter(idea=self)

    def get_all_images(self):
        ''' returns all images for an idea '''

        return Image.objects.filter(idea=self)

    def get_all_drawings(self):
        ''' returns all drawings for an idea '''

        return Drawing.objects.filter(idea=self)
        

class Scene(models.Model):
    ''' models the data attributes of a scene '''

    title = models.TextField()
    outline = models.TextField(blank=True)
    script = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE) # linking the Scene model to the Idea model with a foreign key

    def __str__(self):
        ''' returns a string representation of the Scene model that is just the title '''
        return f'{self.title}'

    def get_all_characters(self):
        ''' returns all characters for a scene '''

        return Character.objects.filter(scenes=self)

    def get_all_images(self):
        ''' Gets all images for a scene. Returns a queryset of all images that are either tied to the scene or to a character in the scene '''
        
        # returns a queryset of all images that are either tied to the scene or to a character in the scene
        return (
            Image.objects.filter(scene=self) | Image.objects.filter(character__scenes=self)
        ).distinct() # The distinct() method is used to remove duplicate images from the queryset in case there are any images that are tied to both the scene and a character in the scene

    def get_all_drawings(self):
        ''' returns all drawings linked directly to this scene '''
        return Drawing.objects.filter(scene=self)


class Character(models.Model):
    ''' models the data attributes of a character '''

    # Defining the data attributes of the Character model
    name = models.TextField()
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE) # linking the Character model to the Idea model with a foreign key
    scenes = models.ManyToManyField(Scene, blank=True, related_name='characters') # linking the Character model to many Scene rows


    def __str__(self):
        ''' returns a string representation of the Character model that is just the name '''
        return f'{self.name}'

    def get_all_images(self):
        ''' returns all images for a character '''

        return Image.objects.filter(character=self)

    def get_all_drawings(self):
        ''' returns all drawings for a character '''
        return Drawing.objects.filter(character=self)


class Image(models.Model):
    ''' models the data attributes of an image '''

    # Defining the data attributes of the Image model
    image_url = models.URLField(blank=True) # field for the image url
    image_file = models.ImageField( blank=True) # field for the image file
    description = models.TextField(blank=True) # field for the image description
    timestamp = models.DateTimeField(auto_now=True)
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, null=True, blank=True) # linking the Image model to the Scene model with a foreign key
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True, blank=True) # linking the Image model to the Character model with a foreign key
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE) # linking the Image model to the Idea model with a foreign key

    def get_image_url(self):
        ''' returns the image url for an image '''

        if self.image_file: # checking if the image file is not None, and if it exists, return the image file url
            return self.image_file.url
        else: # if the image file does not exist, return the image url
            return self.image_url

    def __str__(self):
        ''' returns a string representation of the Image model that is just the image_url '''
        return f'{self.description}'


class Drawing(models.Model):
    ''' models the data attributes for an Excalidraw drawing '''

    title = models.TextField(blank=True) # optional title
    scene_data = models.JSONField(default=dict, blank=True) # saved Excalidraw scene JSON used to reopen and continue editing
    thumbnail_data_url = models.TextField(blank=True) # small preview image generated in the browser for the drawing
    timestamp = models.DateTimeField(auto_now=True)
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, null=True, blank=True) # linking the Drawing model to the Scene model with a foreign key
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True, blank=True) # linking the Drawing model to the Character model with a foreign key
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE) # linking the Drawing model to the Idea model with a foreign key

    def __str__(self):
        ''' returns a string representation of the Drawing model '''

        if self.title: # if the title is not empty, return the title
            return f'{self.title}'
        return f'Drawing {self.pk}' # if the title is empty, return the drawing id