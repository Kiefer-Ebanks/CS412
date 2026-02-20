# File: forms.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 2/20/2026
# Description: The forms file for the mini instagram app
# Creating the forms for the mini instagram app

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    ''' A form to create a new post '''

    class Meta:
        model = Post
        fields = ['caption']
