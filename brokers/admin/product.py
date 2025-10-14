from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from ..models import Product, ProductImage, ProductView, ProductInquiry


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1
    max_num = 10
    fields = ['image', 'caption', 'is_main', 'order']
    ordering = ['order', '-is_main']


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = [
        'get_main_image_preview', 'title', 'brand', 'model', 
        'category', 'formatted_price', 'location_city', 'seller', 
        'is_active', 'is_sold', 'view_count', 'contact_link'
    ]
    list_filter = [
        'category', 'condition', 'is_active', 'is_sold', 'is_featured', 
        'created_at', 'location_province', 'currency'
    ]
    search_fields = ['title', 'brand', 'model', 'description', 'contact_name']
    readonly_fields = ['slug', 'whatsapp_link', 'view_count', 'created_at', 'updated_at']
    
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = [
        ('Informasi Dasar', {
            'fields': ['title', 'category', 'seller']
        }),
        ('Auto Generated', {
            'fields': ['slug'],
            'classes': ['collapse']
        }),
        ('Detail Produk', {
            'fields': [
                ('brand', 'model'),
                'condition',
                'attributes'
            ]
        }),
        ('Lokasi', {
            'fields': [
                ('location_city', 'location_province'),
                'location_detail'
            ]
        }),
        ('Harga', {
            'fields': [('price', 'currency'), 'is_negotiable']
        }),
        ('Kontak', {
            'fields': [
                ('contact_name', 'contact_phone'),
                'contact_email'
            ]
        }),
        ('Link WhatsApp', {
            'fields': ['whatsapp_link'],
            'classes': ['collapse']
        }),
        ('Deskripsi', {
            'fields': ['description']
        }),
        ('Status', {
            'fields': ['is_active', 'is_featured', 'is_sold']
        }),
        ('SEO', {
            'fields': ['meta_title', 'meta_description'],
            'classes': ['collapse']
        }),
        ('Analytics', {
            'fields': ['view_count'],
            'classes': ['collapse']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    
    inlines = [ProductImageInline]
    actions = ['mark_as_sold', 'mark_as_available', 'mark_as_featured']
    
    @display(description='Gambar Utama')
    def get_main_image_preview(self, obj):
        main_image = obj.main_image
        if main_image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 45px; object-fit: cover; border-radius: 4px;" />',
                main_image.image.url
            )
        return format_html(
            '<div style="width: 60px; height: 45px; background: #f0f0f0; border-radius: 4px; '
            'display: flex; align-items: center; justify-content: center; font-size: 12px; color: #666;">'
            'No Image</div>'
        )
    
    @display(description='Harga')
    def formatted_price(self, obj):
        return obj.formatted_price
    
    @display(description='Views')
    def view_count(self, obj):
        return obj.views.count()
    
    @display(description='Kontak')
    def contact_link(self, obj):
        return format_html(
            '<a href="{}" target="_blank" style="color: #25D366; text-decoration: none;">📱 WhatsApp</a>',
            obj.whatsapp_link
        )
    
    def mark_as_sold(self, request, queryset):
        queryset.update(is_sold=True, is_active=False)
        self.message_user(request, f"{queryset.count()} produk ditandai sebagai terjual.")
    mark_as_sold.short_description = "Tandai sebagai terjual"
    
    def mark_as_available(self, request, queryset):
        queryset.update(is_sold=False, is_active=True)
        self.message_user(request, f"{queryset.count()} produk ditandai sebagai tersedia.")
    mark_as_available.short_description = "Tandai sebagai tersedia"
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} produk ditandai sebagai unggulan.")
    mark_as_featured.short_description = "Tandai sebagai produk unggulan"


@admin.register(ProductImage)
class ProductImageAdmin(ModelAdmin):
    list_display = ['get_image_preview', 'product', 'caption', 'is_main', 'order', 'created_at']
    list_filter = ['is_main', 'created_at', 'product__category']
    search_fields = ['product__title', 'caption']
    list_editable = ['is_main', 'order', 'caption']
    
    @display(description='Preview')
    def get_image_preview(self, obj):
        return format_html(
            '<img src="{}" style="width: 80px; height: 60px; object-fit: cover; border-radius: 4px;" />',
            obj.image.url
        )

@admin.register(ProductView)
class ProductViewAdmin(ModelAdmin):
    list_display = ['product', 'ip_address', 'session_key', 'viewed_at']
    list_filter = ['viewed_at', 'product__category']
    search_fields = ['product__title', 'ip_address']
    readonly_fields = ['product', 'ip_address', 'user_agent', 'session_key', 'viewed_at']

@admin.register(ProductInquiry)
class ProductInquiryAdmin(ModelAdmin):
    list_display = ['product', 'inquirer_name', 'inquirer_phone', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'product__category']
    search_fields = ['product__title', 'inquirer_name', 'inquirer_phone', 'message']
    readonly_fields = ['created_at']
    list_editable = ['status']
    
    fieldsets = [
        ('Informasi Inquiry', {
            'fields': ['product', 'inquirer_name', 'inquirer_phone', 'inquirer_email', 'status']
        }),
        ('Pesan', {
            'fields': ['message']
        }),
        ('Timestamps', {
            'fields': ['created_at']
        })
    ]
