from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


@extend_schema(
    responses={200: dict},
    tags=['General']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint
    
    Returns the current health status of the API.
    """
    return Response({
        'status': 'healthy',
        'message': 'API is running successfully'
    })


@extend_schema(
    responses={200: dict},
    tags=['General']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """
    API information endpoint
    
    Returns basic information about the API including available endpoints.
    """
    return Response({
        'name': 'Core Backend API',
        'version': '1.0.0',
        'description': 'Django REST API with JWT authentication',
        'docs': {
            'swagger': '/api/docs/',
            'redoc': '/api/redoc/',
            'schema': '/api/schema/'
        },
        'endpoints': {
            'auth': '/api/auth/',
            'health': '/api/health/',
        }
    })
