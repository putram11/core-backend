from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    Profile model with one-to-one relationship to Django's built-in User model
    Contains additional user information like phone, profile picture, etc.
    """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Nomor Telepon")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Tanggal Lahir")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name="Foto Profil")
    bio = models.TextField(max_length=500, blank=True, verbose_name="Bio")
    website = models.URLField(blank=True, verbose_name="Website")
    location = models.CharField(max_length=100, blank=True, verbose_name="Lokasi")
    is_verified = models.BooleanField(default=False, verbose_name="Terverifikasi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'Profil Pengguna'
        verbose_name_plural = 'Profil Pengguna'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Profil {self.user.username}"
    
    @property
    def full_name(self):
        """Returns the user's full name from the related User model."""
        return f"{self.user.first_name} {self.user.last_name}".strip()
    
    @property
    def display_name(self):
        """Returns display name - full name if available, otherwise username."""
        full_name = self.full_name
        return full_name if full_name else self.user.username
