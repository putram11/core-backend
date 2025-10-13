"""
Utility functions for Core Backend
"""

def environment_callback(request):
    """
    Callback to show current environment in admin
    """
    return ["Development", "success"]  # [text, color]


def dashboard_callback(request):
    """
    Callback for dashboard customization
    """
    return []  # Return empty list for now, can be extended with widgets
