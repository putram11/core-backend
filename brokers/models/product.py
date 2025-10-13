from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from .category import Category
import uuid
import os


User = get_user_model()


def upload_product_image(instance, filename):
    """Upload path for product images"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('products', instance.product.slug, filename)


class Product(models.Model):
    """Flexible product model for any type of items"""
    
    CONDITION_CHOICES = [
        ('new', 'Baru'),
        ('like_new', 'Seperti Baru'),
        ('good', 'Baik'),
        ('fair', 'Cukup Baik'),
        ('poor', 'Perlu Perbaikan'),
    ]
    
    # Basic Info
    title = models.CharField(max_length=200, verbose_name='Judul Produk')
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Kategori')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Penjual')
    
    # Product Details
    brand = models.CharField(max_length=100, blank=True, verbose_name='Merk/Brand')
    model = models.CharField(max_length=100, blank=True, verbose_name='Model/Tipe')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, verbose_name='Kondisi')
    
    # Flexible attributes stored as JSON
    attributes = models.JSONField(default=dict, blank=True, verbose_name='Atribut Produk', 
                                help_text='Data fleksibel dalam format JSON: {"tahun": "2020", "warna": "Merah", "cc": "150"}')
    
    # Location
    location_city = models.CharField(max_length=100, verbose_name='Kota')
    location_province = models.CharField(max_length=100, verbose_name='Provinsi')
    location_detail = models.TextField(blank=True, verbose_name='Alamat Detail')
    
    # Pricing
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Harga')
    is_negotiable = models.BooleanField(default=True, verbose_name='Bisa Nego')
    currency = models.CharField(max_length=3, default='IDR', verbose_name='Mata Uang')
    
    # Contact Info
    contact_name = models.CharField(max_length=100, verbose_name='Nama Kontak')
    contact_phone = models.CharField(max_length=20, verbose_name='Nomor WhatsApp')
    contact_email = models.EmailField(blank=True, verbose_name='Email')
    
    # Description
    description = models.TextField(verbose_name='Deskripsi Produk')
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name='Status Aktif')
    is_featured = models.BooleanField(default=False, verbose_name='Produk Unggulan')
    is_sold = models.BooleanField(default=False, verbose_name='Sudah Terjual')
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True, verbose_name='Meta Title')
    meta_description = models.TextField(blank=True, verbose_name='Meta Description')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Produk'
        verbose_name_plural = 'Produk'
        ordering = ['-created_at']
        
    def __str__(self):
        if self.brand and self.model:
            return f"{self.brand} {self.model}"
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    @property
    def whatsapp_link(self):
        """Generate WhatsApp link for contacting seller"""
        phone = self.contact_phone.replace('+', '').replace('-', '').replace(' ', '')
        if phone.startswith('0'):
            phone = '62' + phone[1:]  # Convert Indonesian format
        
        product_name = f"{self.brand} {self.model}" if self.brand and self.model else self.title
        message = f"Halo, saya tertarik dengan {product_name} yang Anda jual seharga {self.formatted_price}"
        
        # URL encode the message
        import urllib.parse
        encoded_message = urllib.parse.quote(message)
        return f"https://wa.me/{phone}?text={encoded_message}"
    
    @property
    def main_image(self):
        """Get the first/main image of the product"""
        return self.images.filter(is_main=True).first() or self.images.first()
    
    @property
    def formatted_price(self):
        """Format price based on currency"""
        if self.currency == 'IDR':
            return f"Rp {self.price:,.0f}"
        elif self.currency == 'USD':
            return f"${self.price:,.2f}"
        elif self.currency == 'EUR':
            return f"€{self.price:,.2f}"
        else:
            return f"{self.currency} {self.price:,.2f}"
    
    def get_attribute(self, key, default=None):
        """Get specific attribute from JSON field"""
        return self.attributes.get(key, default)
    
    def set_attribute(self, key, value):
        """Set specific attribute in JSON field"""
        if not self.attributes:
            self.attributes = {}
        self.attributes[key] = value


class ProductImage(models.Model):
    """Product images - maximum 10 per product"""
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Produk')
    image = models.ImageField(upload_to=upload_product_image, verbose_name='Gambar')
    caption = models.CharField(max_length=200, blank=True, verbose_name='Caption')
    is_main = models.BooleanField(default=False, verbose_name='Gambar Utama')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Gambar Produk'
        verbose_name_plural = 'Gambar Produk'
        ordering = ['order', '-is_main', 'created_at']
        
    def __str__(self):
        return f"Image {self.order} for {self.product}"
    
    def save(self, *args, **kwargs):
        # Ensure only one main image per product
        if self.is_main:
            ProductImage.objects.filter(product=self.product, is_main=True).update(is_main=False)
        
        # Validate maximum 10 images per product
        if not self.pk:  # New image
            existing_count = ProductImage.objects.filter(product=self.product).count()
            if existing_count >= 10:
                raise ValueError("Maksimal 10 gambar per produk")
        
        super().save(*args, **kwargs)


class ProductView(models.Model):
    """Track product views for analytics"""
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='views')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'View Produk'
        verbose_name_plural = 'View Produk'
        unique_together = ['product', 'ip_address', 'session_key']
        
    def __str__(self):
        return f"View for {self.product} from {self.ip_address}"


class ProductInquiry(models.Model):
    """Track inquiries made through WhatsApp links"""
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inquiries')
    inquirer_name = models.CharField(max_length=100, blank=True, verbose_name='Nama Penanya')
    inquirer_phone = models.CharField(max_length=20, blank=True, verbose_name='Nomor HP')
    inquirer_email = models.EmailField(blank=True, verbose_name='Email Penanya')
    message = models.TextField(blank=True, verbose_name='Pesan')
    status = models.CharField(max_length=20, choices=[
        ('new', 'Baru'),
        ('replied', 'Sudah Dibalas'),
        ('closed', 'Ditutup')
    ], default='new', verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Inquiry Produk'
        verbose_name_plural = 'Inquiry Produk'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Inquiry for {self.product} from {self.inquirer_name or 'Anonymous'}"
