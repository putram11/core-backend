from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from unfold.admin import ModelAdmin # type: ignore
from unfold.decorators import display # pyright: ignore[reportMissingImports]
from ..models import Category


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'parent', 'get_image_preview', 'icon', 'color_badge', 'is_active', 'is_featured', 'product_count', 'sort_order']
    list_filter = ['is_active', 'is_featured', 'parent', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['slug', 'created_at', 'updated_at', 'full_path']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['sort_order', 'is_active', 'is_featured']
    
    fieldsets = [
        ('Informasi Dasar', {
            'fields': ['name', 'slug', 'parent', 'description', 'full_path']
        }),
        ('Tampilan', {
            'fields': ['image', 'icon', 'color']
        }),
        ('Status', {
            'fields': ['is_active', 'is_featured', 'sort_order']
        }),
        ('SEO', {
            'fields': ['meta_title', 'meta_description'],
            'classes': ['collapse']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    
    @display(description='Preview Gambar')
    def get_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        elif obj.icon:
            return format_html(
                '<i class="{}" style="font-size: 24px; color: {};"></i>',
                obj.icon, obj.color
            )
        return '-'
    
    @display(description='Warna')
    def color_badge(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background: {}; border-radius: 50%; border: 1px solid #ddd;"></div>',
            obj.color
        )
    
    @display(description='Jumlah Produk')
    def product_count(self, obj):
        count = obj.product_set.count()
        if count > 0:
            url = reverse('admin:brokers_product_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} produk</a>', url, count)
        return '0 produk'
