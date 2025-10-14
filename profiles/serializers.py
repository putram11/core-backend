from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for Django's built-in User model"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model"""
    
    user = UserSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()
    display_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Profile
        fields = [
            'user', 'phone_number', 'date_of_birth', 'profile_picture', 
            'bio', 'website', 'location', 'is_verified', 'full_name', 
            'display_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_verified']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating Profile"""
    
    class Meta:
        model = Profile
        fields = [
            'phone_number', 'date_of_birth', 'profile_picture', 
            'bio', 'website', 'location'
        ]
