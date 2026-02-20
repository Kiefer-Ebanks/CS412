from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView # Importing the ListView and DetailView classes
from .models import Profile, Post # Importing the Profile and Post models from the models.py file
from .forms import CreatePostForm # Importing the CreatePostForm from the forms.py file
# Create your views here.


class ProfileListView(ListView):
    ''' A view to display a list of all profiles '''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles' # using plural variable name for the profiles list


class ProfileDetailView(DetailView):
    ''' A view to display a single profile '''

    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile' # using singular variable name for the profile object


class PostDetailView(DetailView):
    ''' A view to display a single post '''

    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post' # using singular variable name for the post object


class CreatePostView(CreateView):
    ''' A view to create a new post '''

    model = Post
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'
    context_object_name = 'post' # using singular variable name for the post object
    
    def get_context_data(self, **kwargs):
        ''' Add profile object to context '''
        context = super().get_context_data(**kwargs) # getting the context dictionary from the parent class
        profile = Profile.objects.get(pk=self.kwargs['pk']) # getting the profile object using the pk from the URL parameters
        context['profile'] = profile # adding the profile object to the context
        return context