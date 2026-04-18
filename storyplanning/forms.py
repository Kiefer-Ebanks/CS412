# File: forms.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 4/17/2026
# Description: The forms file for the story planning app

from django import forms
from .models import Idea

class CreateIdeaForm(forms.ModelForm):
    ''' A form to create an idea '''

    class Meta:
        model = Idea
        fields = ['title', 'storyboard']