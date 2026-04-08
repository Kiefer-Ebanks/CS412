# File: serializers.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 4/7/2026
# Description: The serializers for the mini instagram app and the API endpoints

from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    ''' serializer class to convert a user from django model instance to JSON for API '''

    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        ''' create a new user '''

        # validated_data is the data that is passed in from the client
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    ''' serializer class to convert a profile from django model instance to JSON for API '''
    
    class Meta:
        model = Profile
        fields = ['id', 'username', 'display_name', 'profile_image_url', 'bio_text', 'join_date']

# PhotoSerializer is used to serialize the photos for a single Post
class PhotoSerializer(serializers.ModelSerializer):
    ''' serializer class to convert a photo from django model instance to JSON for API '''

    # image is not a field in the Photo model, so creating serializer method field to serialize post images
    image = serializers.SerializerMethodField() # so when the PostSerializer is serialized, the images field will be serialized as a list of PhotoSerializer objects
    # and the django Rest Framework will call the get_image method automatically to get the image url for a photo

    class Meta:
        model = Photo
        fields = ['id', 'post', 'image'] # including the pk, post, and image fields

    def get_image(self, obj): # because the image is not a field in the Photo model, we need to use a serializer method field to serialize it
        return obj.get_image_url() # calling my object method to get the image_url for a photo (whether it is a URL or a file)


class PostSerializer(serializers.ModelSerializer):
    ''' serializer class to convert a post from django model instance to JSON for API '''

    # using the Post to Photo reverse FK relation to get each Post's related Photo rows as photo_set
    # then use the PhotoSerializer to serialize each Photo as images
    images = PhotoSerializer(many=True, read_only=True, source='photo_set') # many=True to be able to serialize multiple photos and read-only=True to prevent users from changing the images
    files = serializers.ImageField(write_only=True, required=False) # files is used to upload multiple images to the post

    class Meta:
        model = Post
        fields = ['id', 'profile', 'images', 'files', 'caption', 'timestamp'] # including the pk, profile, images, files, caption, and timestamp fields

    # adding this method to be able to create a post object
    def create(self, validated_data):
        ''' Override the superclass method that handles object creation. '''

        # get the request from the context
        request = self.context.get('request')

        # check if the request is None or if the user is not authenticated
        if request == None or request.user.is_authenticated == False:
            raise serializers.ValidationError('Authentication required to create a post.')

        profile = Profile.objects.filter(user=request.user).order_by('pk').first()
        if profile == None:
            raise serializers.ValidationError({'profile': 'No profile exists for this user.'})

        post = Post.objects.create(profile=profile, **validated_data)

        # create one related Photo object per uploaded file
        files = request.FILES.getlist('files')
        for file in files:
            Photo.objects.create(post=post, image_file=file)

        return post

# class FeedSerializer(serializers.ModelSerializer):
#     ''' serializer class to convert a feed from django model instance to JSON for API '''
    
#     class Meta:
#         model = Post
#         fields = ['id', 'profile', 'caption', 'timestamp'] # including the pk, profile, caption, and timestamp fields

                