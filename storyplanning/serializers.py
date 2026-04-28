# File: serializers.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 4/24/2026
# Description: The serializers for the story planning app

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Idea, Scene, Character, Image


class UserSerializer(serializers.ModelSerializer):
    ''' serializer class to convert a user from django model instance to JSON for API '''

    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=False,
        style={'input_type': 'password'}, # allows the password to be input as a password field in the browser so the input is not visible to the user when they are typing it in
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        ''' create a new user
        validated_data is the data that is passed in from the client'''

        if not validated_data.get('password'): # checks the password is in the validated data
            raise serializers.ValidationError({'password': 'This field is required when registering'})

        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

    def update(self, instance, validated_data):
        ''' updating a user's username, email, and password '''

        instance.username = validated_data.get('username', instance.username)

        if 'password' in validated_data and validated_data['password']: # checks the password is in the validated data
            instance.set_password(validated_data['password']) # sets the password for the instance but uses the set_password method to hash the password
        
        instance.save()
        return instance


class ImageSerializer(serializers.ModelSerializer):
    '''
    serializer class to convert an image from django model instance to JSON for API 
    image: returns a read-only field for the image url or file so viewers can see the image
    image_url and image_file: serializer fields for creating and updating the images
    '''

    image = serializers.SerializerMethodField(read_only=True) # because the image is not a field in the Image model, we need to use a serializer method field to serialize it
    image_url = serializers.URLField(allow_blank=True, required=False)
    image_file = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = Image
        fields = ['id', 'image', 'image_url', 'image_file', 'description', 'timestamp', 'scene', 'character', 'idea']
        read_only_fields = ['timestamp']

    def get_image(self, obj):
        ''' returns the image url for an image
        The django Rest Framework will call the get_image method automatically to get the image url for an image when the ImageSerializer is serialized'''
        
        if obj:
            return obj.get_image_url()
        else:
            return None


class CharacterSerializer(serializers.ModelSerializer):
    ''' serializer class to convert a character from django model instance to JSON for API '''

    class Meta:
        model = Character
        fields = ['id', 'name', 'description', 'timestamp', 'idea', 'scene']
        read_only_fields = ['timestamp']


class SceneSerializer(serializers.ModelSerializer):
    ''' serializer class to convert a scene from django model instance to JSON for API '''

    characters = CharacterSerializer(many=True, read_only=True, source='get_all_characters')
    images = ImageSerializer(many=True, read_only=True, source='get_all_images')

    class Meta:
        model = Scene
        fields = ['id', 'title', 'outline', 'script', 'timestamp', 'idea', 'characters', 'images']
        read_only_fields = ['timestamp']


class IdeaSerializer(serializers.ModelSerializer):
    ''' serializer class to convert an idea from django model instance to JSON for API '''

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    scenes = SceneSerializer(many=True, read_only=True, source='get_all_scenes')
    characters = CharacterSerializer(many=True, read_only=True, source='get_all_characters')
    images = ImageSerializer(many=True, read_only=True, source='get_all_images')

    class Meta:
        model = Idea
        fields = ['id', 'title', 'storyboard', 'timestamp', 'user', 'scenes', 'characters', 'images']
        read_only_fields = ['timestamp', 'user']

    def create(self, validated_data):
        ''' creating a new idea for the current user '''

        user = self.context['request'].user
        if not user or not user.is_authenticated:
            raise serializers.ValidationError('Authentication required')

        validated_data['user'] = user # adding the user to the validated data
        return super().create(validated_data)

    def update(self, instance, validated_data):
        ''' update an idea's title and storyboard '''

        for field in ('title', 'storyboard'):
            if field in validated_data:
                setattr(instance, field, validated_data[field]) # setting the field to the validated data for the instance from the client's request
        instance.save()
        return instance
