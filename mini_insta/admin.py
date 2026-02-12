from django.contrib import admin

# Register your models here.

# Importing the Profile model from the models.py file
from .models import Profile

# Registering the Profile model with the admin site
admin.site.register(Profile)