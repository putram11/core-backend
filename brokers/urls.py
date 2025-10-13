from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ProductInquiryViewSet

app_name = 'brokers'

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'inquiries', ProductInquiryViewSet, basename='inquiry')

urlpatterns = [
    path('api/', include(router.urls)),
]
