# File: views.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 4/2/2026
# Description: The views for the dad jokes app and the API endpoints

from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Joke, Picture
import random


class RandomView(DetailView):
    ''' DetailView for Joke: URL may include pk (DB lookup) or omit it (random joke). '''

    model = Joke
    template_name = 'dadjokes/random.html'
    context_object_name = 'joke'

    def get_object(self, queryset=None):
        qs = self.get_queryset() if queryset is None else queryset
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            return get_object_or_404(qs, pk=pk)
        return random.choice(list(qs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['picture'] = random.choice(list(Picture.objects.all()))
        return context

class DadJokesListView(ListView):
    ''' A ListView that displays a list of all dad jokes '''
    model = Joke
    template_name = 'dadjokes/jokes.html'
    context_object_name = 'jokes'

class DadJokeDetailView(DetailView):
    ''' A DetailView that displays a single dad joke '''
    model = Joke
    template_name = 'dadjokes/one_joke.html'
    context_object_name = 'joke'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['random_joke'] = random.choice(list(Joke.objects.all()))
        return context

class PicturesListView(ListView):
    ''' A ListView that displays a list of all pictures '''

    model = Picture
    template_name = 'dadjokes/pictures.html'
    context_object_name = 'pictures'

class PictureDetailView(DetailView):
    ''' A DetailView that displays a single picture '''

    model = Picture
    template_name = 'dadjokes/one_picture.html'
    context_object_name = 'picture'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['random_picture'] = random.choice(list(Picture.objects.all()))
        return context