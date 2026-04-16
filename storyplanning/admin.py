# File: admin.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 4/16/2026
# Description: The admin file for the story planning app
# Creating the admin for the story planning app

from django.contrib import admin

# Importing the models from the models.py file
from .models import Idea
from .models import Scene
from .models import Character
from .models import Image

# Registering the models with the admin site
admin.site.register(Idea)
admin.site.register(Scene)
admin.site.register(Character)
admin.site.register(Image)
