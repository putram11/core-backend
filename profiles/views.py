from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile
from .serializers import ProfileSerializer, ProfileUpdateSerializer, UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for Profile model"""
    
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return profiles based on user permissions"""
        if self.request.user.is_superuser:
            return Profile.objects.all()
        return Profile.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer class based on action"""
        if self.action in ['update', 'partial_update']:
            return ProfileUpdateSerializer
        return ProfileSerializer
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Get or update current user's profile"""
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            # Create profile if it doesn't exist
            profile = Profile.objects.create(user=request.user)
        
        if request.method == 'GET':
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = ProfileUpdateSerializer(profile, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                return Response(ProfileSerializer(profile).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def user_info(self, request):
        """Get current user's basic information"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
