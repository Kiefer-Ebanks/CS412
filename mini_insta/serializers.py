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
    ''' serializer class to convert an article from django model instance to JSON for API '''
    
    class Meta:
        model = Profile
        fields = ['id', 'username', 'display_name', 'profile_image_url', 'bio_text', 'join_date']

        