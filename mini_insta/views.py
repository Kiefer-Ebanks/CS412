from django.shortcuts import render
from django.urls import reverse # Importing the reverse function to redirect to the profile page

from django.views.generic import ListView, DetailView, CreateView, UpdateView # Importing the ListView and DetailView classes
from .models import Profile, Post, Photo # Importing the Profile, Photo, and Post models from the models.py file
from .forms import CreatePostForm # Importing the CreatePostForm from the forms.py file
from .forms import UpdateProfileForm # Importing the UpdateProfileForm from the forms.py file
from django.urls import reverse # Importing the reverse function to redirect to the profile page
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

    def form_valid(self, form):
        ''' Add profile object to post and create the photo object if provided '''

        pk = self.kwargs['pk']

        profile = Profile.objects.get(pk=pk) # Get the profile object from the URL parameters
        form.instance.profile = profile # Add the profile object to the post instance
        
        post = form.save() # save the post so it has a pk in the database
        
        # Commenting out the previous image_url code for now to focus on the image_file code
        # image_url = self.request.POST.get('image_url', '') # getting the image_url from the POST request
        
        # if image_url:
        #     Photo.objects.create(post=post, image_url=image_url) # create a new Photo object with the saved post as the foreign key

        # Read the data from self.request.FILES
        files = self.request.FILES.getlist('files')
        for file in files:
            Photo.objects.create(post=post, image_file=file) # create a new Photo object for each file with the saved post as the foreign key

        return super().form_valid(form) # delegate work to the super class of the form_valid method

    def get_success_url(self):
        ''' Redirect to the profile page '''
        return reverse('show_post', kwargs={'pk': self.object.pk}) # redirect to the show_post view with the pk of the post that was just created


class UpdateProfileView(UpdateView):
    ''' A view to update a profile '''

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'
    context_object_name = 'profile' # using singular variable name for the profile object