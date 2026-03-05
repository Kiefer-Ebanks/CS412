from django.shortcuts import render
from django.urls import reverse # Importing the reverse function to redirect to the profile page
from django.http import Http404 # Importing the Http404 class to raise a 404 error if the profile does not exist
from django.db.models import Q # Importing the Q object to filter the profiles and posts

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView # Importing the ListView, DetailView, CreateView, UpdateView, DeleteView, and TemplateView classes
from .models import Profile, Post, Photo # Importing the Profile, Photo, and Post models from the models.py file
from .forms import CreatePostForm, UpdatePostForm # Importing the CreatePostForm and UpdatePostForm from the forms.py file
from .forms import UpdateProfileForm # Importing the UpdateProfileForm from the forms.py file
from django.urls import reverse # Importing the reverse function to redirect to the profile page

from django.contrib.auth.mixins import LoginRequiredMixin # Will use to ensure a user is logged in in order to view the page
from django.contrib.auth.views import LogoutView # Will use to log out the user and redirect to the logged out page


# Create your views here.

class myLoginRequiredMixin(LoginRequiredMixin):
    ''' A custom login required mixin that redirects to the login page if the user is not logged in '''

    def get_login_url(self):
        ''' Redirect to the login page '''
        return reverse('login') # redirect to the login view


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

    def get_context_data(self, **kwargs):
        ''' Add profile object to context based on this post '''
        context = super().get_context_data(**kwargs)
        post = self.object
        context['profile'] = post.profile
        return context


class CreatePostView(myLoginRequiredMixin, CreateView):
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

    def get_login_url(self):
        ''' Redirect to the login page '''
        return reverse('login') # redirect to the login view


class UpdateProfileView(myLoginRequiredMixin, UpdateView):
    ''' A view to update a profile '''

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'
    context_object_name = 'profile' # using singular variable name for the profile object

class DeletePostView(myLoginRequiredMixin, DeleteView):
    ''' A view to delete a post '''

    model = Post
    template_name = 'mini_insta/delete_post_form.html'
    context_object_name = 'post' # using singular variable name for the post object

    def get_context_data(self, **kwargs):
        ''' Add profile object to context based on this post '''
        context = super().get_context_data(**kwargs)
        post = self.object
        context['profile'] = post.profile
        return context

    def get_success_url(self):
        ''' Redirect to the profile page '''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk}) # redirect to the show_profile view with the pk of the profile that the post belongs to


class UpdatePostView(myLoginRequiredMixin, UpdateView):
    ''' A view to update a post '''

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'
    context_object_name = 'post' # using singular variable name for the post object

    def get_context_data(self, **kwargs):
        ''' Add profile object to context based on this post '''
        context = super().get_context_data(**kwargs)
        post = self.object
        context['profile'] = post.profile
        return context

    def get_success_url(self):
        ''' Redirect to the post page '''
        return reverse('show_post', kwargs={'pk': self.object.pk}) # redirect to the show_post view with the pk of the post that was just updated


class ShowFollowersDetailView(DetailView):
    ''' A view to display the followers of a profile '''

    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile' # using singular variable name for the profile object

    def get_context_data(self, **kwargs):
        ''' Add followers to context '''
        context = super().get_context_data(**kwargs)
        profile = self.object
        context['followers'] = profile.get_followers()
        return context


class ShowFollowingDetailView(DetailView):
    ''' A view to display the profiles that a profile follows '''

    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile' # using singular variable name for the profile object

    def get_context_data(self, **kwargs):
        ''' Add following to context '''
        context = super().get_context_data(**kwargs)
        profile = self.object
        context['following'] = profile.get_following()
        return context


class PostFeedListView(myLoginRequiredMixin, ListView):
    ''' A ListView that displays the post feed for a profile (posts from profiles they follow) '''

    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'post_feed'

    def get_queryset(self):
        ''' Return posts from profiles that this profile follows '''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        ''' Add profile to context for the feed heading '''
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context


class SearchView(myLoginRequiredMixin, ListView):
    ''' A ListView for search results (Profiles and Posts). Search is done on behalf of the profile specified by pk. '''

    template_name = 'mini_insta/search_results.html'
    context_object_name = 'object_list'

    def dispatch(self, request, *args, **kwargs):
        ''' If query is absent from GET, show the search form; otherwise run the ListView. '''

        if 'query' not in self.request.GET:
            try:
                profile = Profile.objects.get(pk=self.kwargs['pk'])
            except Profile.DoesNotExist:
                raise Http404("No Profile matches the given query.") # raise a 404 error if the profile does not exist

            return render(request, 'mini_insta/search.html', {'profile': profile})

        return super().dispatch(request, *args, **kwargs) # delegate work to the super class of the dispatch method

    def get_queryset(self):
        ''' Return Posts whose caption contains the search query. '''

        query = self.request.GET['query'].strip() # get the search query from the GET request
        return Post.objects.filter(caption__icontains=query) # return posts whose caption contains the search query

    def get_context_data(self, **kwargs):
        ''' Add profile, query, matching posts, and matching profiles to context. '''

        context = super().get_context_data(**kwargs)
        try:
            profile = Profile.objects.get(pk=self.kwargs['pk'])
        except Profile.DoesNotExist:
            raise Http404("No Profile matches the given query.") # raise a 404 error if the profile does not exist

        query = self.request.GET['query'].strip() # get the search query from the GET request
        context['profile'] = profile
        context['query'] = query
        context['posts'] = self.get_queryset()
        context['profiles'] = Profile.objects.filter(
            Q(username__icontains=query) |
            Q(display_name__icontains=query) |
            Q(bio_text__icontains=query)
        )
        return context

class LoggedOutView(TemplateView):
    ''' A view to display the logged out page '''

    template_name = 'mini_insta/logged_out.html'


