from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile


class ProfileModelTest(TestCase):
    """Test cases for Profile model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
    
    def test_profile_creation(self):
        """Test that profile is created automatically when user is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, Profile)
    
    def test_profile_str_method(self):
        """Test Profile __str__ method"""
        expected = f"Profil {self.user.username}"
        self.assertEqual(str(self.user.profile), expected)
    
    def test_full_name_property(self):
        """Test full_name property"""
        expected = f"{self.user.first_name} {self.user.last_name}"
        self.assertEqual(self.user.profile.full_name, expected)
    
    def test_display_name_property(self):
        """Test display_name property"""
        # Should return full name when available
        expected = f"{self.user.first_name} {self.user.last_name}"
        self.assertEqual(self.user.profile.display_name, expected)
        
        # Should return username when no first/last name
        user_no_name = User.objects.create_user(
            username='noname',
            email='noname@example.com',
            password='testpass123'
        )
        self.assertEqual(user_no_name.profile.display_name, 'noname')
