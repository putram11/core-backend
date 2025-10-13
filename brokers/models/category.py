from django.db import models
from django.utils.text import slugify
import uuid
import os


def upload_category_image(instance, filename):
    """Upload path for category images"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('categories', filename)


class Category(models.Model):
    """Flexible categories for any type of products"""
    
    name = models.CharField(max_length=100, unique=True, verbose_name='Nama Kategori')
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name='Deskripsi')
    image = models.ImageField(upload_to=upload_category_image, blank=True, null=True, verbose_name='Gambar Kategori')
    icon = models.CharField(max_length=50, blank=True, verbose_name='Icon CSS Class', help_text='Misal: fas fa-car, fas fa-motorcycle, dll')
    color = models.CharField(max_length=7, default='#8b5cf6', verbose_name='Warna Tema', help_text='Hex color code')
    
    # Hierarchy support
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children', verbose_name='Kategori Induk')
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name='Status Aktif')
    is_featured = models.BooleanField(default=False, verbose_name='Kategori Unggulan')
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True, verbose_name='Meta Title')
    meta_description = models.TextField(blank=True, verbose_name='Meta Description')
    
    # Order
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategori'
        ordering = ['sort_order', 'name']
        
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def full_path(self):
        """Get full category path"""
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name
    
    def get_all_children(self):
        """Get all children recursively"""
        children = list(self.children.all())
        for child in list(children):
            children.extend(child.get_all_children())
        return children
