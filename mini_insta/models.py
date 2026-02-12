# File: models.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 2/11/2026
# Description: The models file for the mini instagram app
# Creating the models for the mini instagram app

from django.db import models

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


