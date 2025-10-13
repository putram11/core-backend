from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    """Custom User Admin with Unfold theme"""
    
    # Unfold specific settings
    list_fullwidth = True
    warn_unsaved_form = True
    compressed_fields = True
    
    # Forms for Unfold - using default Django forms for now
    
    # Display settings
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active', 'created_at')
    list_display_links = ('email', 'username')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'created_at', 'updated_at')
    list_per_page = 25
    
    # Fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'System generated timestamps for this user'
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'first_name', 'last_name'),
            'description': 'Additional user information'
        }),
    )
    
    # Other settings
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    # Actions
    actions = ['activate_users', 'deactivate_users']
    
    def activate_users(self, request, queryset):
        """Activate selected users"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users have been activated.')
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        """Deactivate selected users"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users have been deactivated.')
    deactivate_users.short_description = "Deactivate selected users"
