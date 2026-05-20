from .models import Notification
from django.conf import settings
import os

def notification_counts(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, read=False).count()
        unread_notifications = Notification.objects.filter(user=request.user, read=False).order_by('-created_at')[:5]
    else:
        unread_count = 0
        unread_notifications = []

    cloud_name = settings.CLOUDINARY_STORAGE.get('CLOUD_NAME', '') or os.environ.get('CLOUDINARY_CLOUD_NAME', '')
    cloud_key = settings.CLOUDINARY_STORAGE.get('API_KEY', '') or os.environ.get('CLOUDINARY_API_KEY', '')
    cloud_secret = settings.CLOUDINARY_STORAGE.get('API_SECRET', '') or os.environ.get('CLOUDINARY_API_SECRET', '')
    cloudinary_configured = bool(os.environ.get('CLOUDINARY_URL') or (cloud_name and cloud_key and cloud_secret))

    return {
        "unread_count": unread_count,
        "unread_notifications": unread_notifications,
        "cloudinary_storage_backend": settings.DEFAULT_FILE_STORAGE,
        "cloudinary_configured": cloudinary_configured,
        "cloudinary_debug": settings.DEBUG or request.user.is_staff,
    }
