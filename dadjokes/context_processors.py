# File: context_processors.py
# Supplies stable nav targets for base.html on every /dadjokes/ page.

from .models import Joke, Picture


def dadjokes_nav(request):
    if not request.path.startswith('/dadjokes'):
        return {}
    return {
        'nav_joke': Joke.objects.order_by('pk').first(),
        'nav_picture': Picture.objects.order_by('pk').first(),
    }
