from django.urls import path
from .views import health_check, api_info

app_name = 'api'

urlpatterns = [
    path('', api_info, name='api_info'),
    path('health/', health_check, name='health_check'),
]
