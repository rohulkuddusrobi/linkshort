from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import string
import random

class ShortURL(models.Model):
    original_url = models.TextField()
    short_code = models.CharField(max_length=10, unique=True)
    custom_alias = models.CharField(max_length=50, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    click_count = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f"{self.short_code} -> {self.original_url[:50]}"
    
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    @classmethod
    def generate_short_code(cls):
        characters = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choices(characters, k=6))
            if not cls.objects.filter(short_code=short_code).exists():
                return short_code
    
    class Meta:
        ordering = ['-created_at']
