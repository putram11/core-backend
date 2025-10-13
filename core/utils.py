"""
Utility functions for Core Backend
"""

def environment_callback(request):
    """
    Callback to show current environment in admin
    """
    return ["Development", "success"]  # [text, color]


def dashboard_callback(request, context):
    """
    Callback for dashboard customization
    """
    return context  # Return the context dict as expected by Unfold
