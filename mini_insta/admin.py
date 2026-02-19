from django.contrib import admin

# Register your models here.

# Importing the Profile model from the models.py file
from .models import Profile
from .models import Post
from .models import Photo

# Registering the Profile model with the admin site
admin.site.register(Profile)

# Registering the Post and Photo models with the admin site
admin.site.register(Post)
admin.site.register(Photo)