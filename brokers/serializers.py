from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductInquiry


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(source='product_set.count', read_only=True)
    full_path = serializers.CharField(read_only=True)
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'image', 'icon', 'color',
            'parent', 'is_active', 'is_featured', 'sort_order', 'product_count',
            'full_path', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'caption', 'is_main', 'order', 'created_at']
        read_only_fields = ['created_at']


class ProductListSerializer(serializers.ModelSerializer):
    main_image = ProductImageSerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    formatted_price = serializers.CharField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'brand', 'model', 'condition',
            'price', 'formatted_price', 'currency', 'is_negotiable',
            'location_city', 'location_province', 'category_name',
            'main_image', 'is_featured', 'created_at'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    formatted_price = serializers.CharField(read_only=True)
    whatsapp_link = serializers.CharField(read_only=True)
    view_count = serializers.IntegerField(source='views.count', read_only=True)
    seller_name = serializers.CharField(source='seller.get_full_name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'brand', 'model', 'condition', 'attributes',
            'price', 'formatted_price', 'currency', 'is_negotiable',
            'location_city', 'location_province', 'location_detail',
            'contact_name', 'contact_phone', 'contact_email', 'whatsapp_link',
            'description', 'category', 'images', 'is_featured', 'view_count',
            'seller_name', 'created_at', 'updated_at'
        ]


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
        max_length=10
    )
    
    class Meta:
        model = Product
        fields = [
            'title', 'category', 'brand', 'model', 'condition', 'attributes',
            'price', 'currency', 'is_negotiable', 'location_city', 'location_province',
            'location_detail', 'contact_name', 'contact_phone', 'contact_email',
            'description', 'meta_title', 'meta_description', 'images', 'uploaded_images'
        ]
    
    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        product = Product.objects.create(**validated_data)
        
        # Create product images
        for index, image in enumerate(uploaded_images):
            ProductImage.objects.create(
                product=product,
                image=image,
                order=index,
                is_main=(index == 0)  # First image is main
            )
        
        return product
    
    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        
        # Update product fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Add new images if provided
        if uploaded_images:
            existing_count = instance.images.count()
            for index, image in enumerate(uploaded_images):
                if existing_count + index < 10:  # Max 10 images
                    ProductImage.objects.create(
                        product=instance,
                        image=image,
                        order=existing_count + index
                    )
        
        return instance


class ProductInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInquiry
        fields = [
            'id', 'product', 'inquirer_name', 'inquirer_phone', 
            'inquirer_email', 'message', 'status', 'created_at'
        ]
        read_only_fields = ['created_at']
