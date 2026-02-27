# File: models.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 2/11/2026
# Description: The models file for the mini instagram app
# Creating the models for the mini instagram app

from django.db import models
#from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    ''' models the data attributes of an individual user '''

    # Defining the data attributes of the Profile model
    username = models.TextField()
    display_name = models.TextField()
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField()
    join_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        ''' returns a string representation of the Profile model '''
        return f'{self.username}'

    def get_all_posts(self):
        ''' returns all posts for a profile '''
        return Post.objects.filter(profile=self).order_by('timestamp')

class Post(models.Model):
    ''' models the data attributes of a post '''

    # Defining the data attributes of the Post model
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        ''' returns a string representation of the Post model '''
        return f'{self.caption}'

    def get_all_photos(self):
        ''' returns all photos for a post '''
        return Photo.objects.filter(post=self)

    #def get_absolute_url(self):
    #    ''' returns the absolute url for a post '''
    #    return reverse('show_post', kwargs={'pk': self.pk})


class Photo(models.Model):
    ''' models the data attributes of a photo '''

    # Defining the data attributes of the Photo model
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField( blank=True) # new field for the image file
    timestamp = models.DateTimeField(auto_now=True)

    def get_image_url(self):
        ''' returns the image url for a photo '''
        if self.image_file:
            return self.image_file.url
        else:
            return self.image_url

    def __str__(self):
        ''' returns a string representation of the Photo model '''
        return f'{self.get_image_url()}'

        
    
