from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    """Profile Admin with Unfold theme"""
    
    # Unfold specific settings
    list_fullwidth = True
    warn_unsaved_form = True
    compressed_fields = True
    
    # Display settings
    list_display = ('user', 'display_name', 'phone_number', 'location', 'is_verified', 'created_at')
    list_display_links = ('user', 'display_name')
    list_filter = ('is_verified', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone_number')
    ordering = ('-created_at',)
    list_per_page = 25
    
    # Fieldsets
    fieldsets = (
        ('User Information', {
            'fields': ('user',),
            'description': 'Associated Django user account'
        }),
        ('Personal Information', {
            'fields': ('phone_number', 'date_of_birth', 'location', 'bio'),
            'description': 'Personal details and contact information'
        }),
        ('Media & Links', {
            'fields': ('profile_picture', 'website'),
            'description': 'Profile picture and external links'
        }),
        ('Verification & Status', {
            'fields': ('is_verified',),
            'description': 'Account verification status'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'System generated timestamps'
        }),
    )
    
    # Read-only fields
    readonly_fields = ('created_at', 'updated_at')
    
    # Actions
    actions = ['verify_profiles', 'unverify_profiles']
    
    def verify_profiles(self, request, queryset):
        """Verify selected profiles"""
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} profiles have been verified.')
    verify_profiles.short_description = "Verify selected profiles"
    
    def unverify_profiles(self, request, queryset):
        """Unverify selected profiles"""
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} profiles have been unverified.')
    unverify_profiles.short_description = "Unverify selected profiles"
