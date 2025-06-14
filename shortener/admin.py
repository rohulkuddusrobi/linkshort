from django.contrib import admin
from .models import ShortURL

@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ['short_code', 'original_url_preview', 'click_count', 'created_at', 'expires_at', 'user']
    list_filter = ['created_at', 'expires_at']
    search_fields = ['short_code', 'original_url', 'custom_alias']
    readonly_fields = ['created_at', 'click_count']
    
    def original_url_preview(self, obj):
        return obj.original_url[:50] + "..." if len(obj.original_url) > 50 else obj.original_url
    original_url_preview.short_description = 'Original URL'
