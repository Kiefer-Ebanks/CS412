from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    ''' serializer class to convert an article from django model instance to JSON for API '''
    class Meta:
        model = Profile
        fields = ['id', 'username', 'display_name', 'profile_image_url', 'bio_text', 'join_date']