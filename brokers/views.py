from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q
from .models import Category, Product, ProductView, ProductInquiry
from .serializers import (
    CategorySerializer, ProductListSerializer, ProductDetailSerializer,
    ProductCreateUpdateSerializer, ProductInquirySerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for categories - read only
    """
    queryset = Category.objects.filter(is_active=True).order_by('sort_order', 'name')
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get'])
    def products(self, request, slug=None):
        """Get products in this category"""
        category = self.get_object()
        products = Product.objects.filter(
            category=category,
            is_active=True,
            is_sold=False
        ).order_by('-is_featured', '-created_at')
        
        # Apply filters
        search = request.query_params.get('search')
        if search:
            products = products.filter(
                Q(title__icontains=search) |
                Q(brand__icontains=search) |
                Q(model__icontains=search) |
                Q(description__icontains=search)
            )
        
        # Apply price filter
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        
        # Pagination
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for products with full CRUD operations
    """
    queryset = Product.objects.filter(is_active=True).order_by('-is_featured', '-created_at')
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'condition', 'location_province', 'currency', 'is_negotiable']
    search_fields = ['title', 'brand', 'model', 'description', 'location_city']
    ordering_fields = ['price', 'created_at']
    ordering = ['-is_featured', '-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by sold status
        show_sold = self.request.query_params.get('show_sold', 'false').lower()
        if show_sold != 'true':
            queryset = queryset.filter(is_sold=False)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to track views"""
        response = super().retrieve(request, *args, **kwargs)
        
        # Track view
        product = self.get_object()
        ip_address = self.get_client_ip(request)
        session_key = request.session.session_key or 'anonymous'
        
        ProductView.objects.get_or_create(
            product=product,
            ip_address=ip_address,
            session_key=session_key,
            defaults={'user_agent': request.META.get('HTTP_USER_AGENT', '')}
        )
        
        return response
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_sold(self, request, slug=None):
        """Mark product as sold"""
        product = self.get_object()
        if product.seller != request.user:
            return Response(
                {'detail': 'You can only mark your own products as sold.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        product.is_sold = True
        product.is_active = False
        product.save()
        
        return Response({'detail': 'Product marked as sold.'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_available(self, request, slug=None):
        """Mark product as available"""
        product = self.get_object()
        if product.seller != request.user:
            return Response(
                {'detail': 'You can only mark your own products as available.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        product.is_sold = False
        product.is_active = True
        product.save()
        
        return Response({'detail': 'Product marked as available.'})
    
    @action(detail=True, methods=['post'])
    def inquire(self, request, slug=None):
        """Create an inquiry for the product"""
        product = self.get_object()
        serializer = ProductInquirySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_products(self, request):
        """Get current user's products"""
        products = Product.objects.filter(seller=request.user).order_by('-created_at')
        
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured products"""
        products = Product.objects.filter(
            is_active=True,
            is_sold=False,
            is_featured=True
        ).order_by('-created_at')[:20]
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class ProductInquiryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for product inquiries
    """
    serializer_class = ProductInquirySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see inquiries for their own products
        return ProductInquiry.objects.filter(
            product__seller=self.request.user
        ).order_by('-created_at')
