from django import template
from django.urls import reverse
import qrcode
from io import BytesIO
import base64

register = template.Library()

@register.filter
def qr_code(short_url_obj):
    """Generate QR code for a ShortURL object"""
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        # We need to construct the full URL manually since we don't have request context
        qr.add_data(f"http://127.0.0.1:8000/{short_url_obj.short_code}/")
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Convert to base64 for embedding in HTML
        image_data = base64.b64encode(buffer.getvalue()).decode()
        return image_data
    except:
        return ""
