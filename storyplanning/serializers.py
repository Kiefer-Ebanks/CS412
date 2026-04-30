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


class ChangePasswordSerializer(serializers.Serializer):
    ''' serializer class to validate the current password and new password for the change password endpoint '''

    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=1)


class ChangeUsernameSerializer(serializers.Serializer):
    ''' serializer class to validate username changes '''

    # new username is required to be a write-only field and must be at least 1 character long to prevent empty usernames
    new_username = serializers.CharField(write_only=True, min_length=1) 

class ImageSerializer(serializers.ModelSerializer):
    '''
    serializer class to convert an image from django model instance to JSON for API 
    image: returns a read-only field for the image url or file so viewers can see the image
    image_url and image_file: serializer fields for creating and updating the images
    '''

    image = serializers.SerializerMethodField(read_only=True) # because the image is not a field in the Image model, we need to use a serializer method field to serialize it
    image_url = serializers.URLField(allow_blank=True, required=False)
    image_file = serializers.ImageField(allow_null=True, required=False)

    # read-only labels for the react frontend to display the idea, scene, and character titles
    idea_title = serializers.CharField(source='idea.title', read_only=True)
    scene_title = serializers.SerializerMethodField()
    character_name = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = [
            'id', 'image', 'image_url', 'image_file', 'description', 'timestamp', 'scene', 'character', 'idea', 'idea_title', 'scene_title', 'character_name',
        ]
        read_only_fields = ['timestamp']

    def get_scene_title(self, obj):
        ''' scene FK is optional so we only return the scene's title if it exists '''

        if obj.scene_id:
            return obj.scene.title
        else:
            return None

    def get_character_name(self, obj):
        ''' character FK is optional so we only return the character's name if it exists '''
        if obj.character_id:
            return obj.character.name
        else:
            return None

    def get_image(self, obj):
        ''' returns the image url for an image
        The django Rest Framework will call the get_image method automatically to get the image url for an image when the ImageSerializer is serialized'''

        if not obj:
            return None

        # my function get_image_url() returns a full URL for image_url, but for uploaded files it returns a media path like /media/...
        url = obj.get_image_url()

        if not url:
            return None

        # since react is running on a different port than Django, the media path would break the img src call for the image because the browser would look for /media/... 
        # so instead we build a full URL using the request so the client always gets a proper url for the image
        request = self.context.get('request') # get the request from the context
        
        if request and url.startswith('/'): # if the url starts with a slash, then build a full URL using the request
            return request.build_absolute_uri(url) # build a full URL using the request
        return url


class CharacterSerializer(serializers.ModelSerializer):
    ''' serializer class to convert a character from django model instance to JSON for the API with images for the character '''

    images = ImageSerializer(many=True, read_only=True, source='get_all_images') # using the ImageSerializer to serialize the images for the character
    scenes = serializers.PrimaryKeyRelatedField(many=True, queryset=Scene.objects.all(), required=False) # return and allow updating all linked scene ids for the character
    scene = serializers.SerializerMethodField() # compatibility field so existing clients can still read one scene id (keeping this here because I had some accounts that were created using the old 1:1 Foreign Key relationship)

    class Meta:
        model = Character
        fields = ['id', 'name', 'description', 'timestamp', 'idea', 'scene', 'scenes', 'images']
        read_only_fields = ['timestamp']

    def get_scene(self, obj):
        ''' compatibility helper returning the first linked scene id or None '''

        first_scene = obj.scenes.first()
        if first_scene:
            return first_scene.pk
        return None

    def validate_scenes(self, scenes):
        ''' ensure all selected scenes belong to the same idea as this character '''

        character = self.instance
        idea = character.idea if character else None
        if idea is None:
            idea = self.initial_data.get('idea')
            if idea is not None:
                try:
                    idea = Idea.objects.get(pk=idea)
                except Idea.DoesNotExist:
                    raise serializers.ValidationError('Idea not found')

        if idea is None:
            return scenes

        invalid_scene = next((scene for scene in scenes if scene.idea_id != idea.id), None)
        if invalid_scene is not None:
            raise serializers.ValidationError('Each selected scene must belong to this character idea')
        return scenes


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
