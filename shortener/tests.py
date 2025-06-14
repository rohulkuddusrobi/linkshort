from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ShortURL

class URLShortenerTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_home_page_loads(self):
        """Test that the home page loads successfully"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Shorten Your URL')
    
    def test_url_shortening(self):
        """Test basic URL shortening functionality"""
        response = self.client.post(reverse('home'), {
            'original_url': 'https://www.example.com',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ShortURL.objects.filter(original_url='https://www.example.com').exists())
    
    def test_custom_alias(self):
        """Test URL shortening with custom alias"""
        response = self.client.post(reverse('home'), {
            'original_url': 'https://www.example.com',
            'custom_alias': 'mylink'
        })
        self.assertEqual(response.status_code, 200)
        short_url = ShortURL.objects.get(custom_alias='mylink')
        self.assertEqual(short_url.short_code, 'mylink')
    
    def test_url_redirection(self):
        """Test that shortened URLs redirect correctly"""
        short_url = ShortURL.objects.create(
            original_url='https://www.example.com',
            short_code='abc123'
        )
        response = self.client.get(reverse('redirect_url', args=['abc123']))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://www.example.com')
        
        # Check that click count increased
        short_url.refresh_from_db()
        self.assertEqual(short_url.click_count, 1)
    
    def test_user_authentication(self):
        """Test user login functionality"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
    
    def test_dashboard_requires_login(self):
        """Test that dashboard requires authentication"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Login and try again
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_url_handling(self):
        """Test handling of invalid URLs"""
        response = self.client.post(reverse('home'), {
            'original_url': 'not-a-valid-url',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a valid URL')
    
    def test_duplicate_custom_alias(self):
        """Test that duplicate custom aliases are rejected"""
        ShortURL.objects.create(
            original_url='https://www.example1.com',
            short_code='duplicate',
            custom_alias='duplicate'
        )
        
        response = self.client.post(reverse('home'), {
            'original_url': 'https://www.example2.com',
            'custom_alias': 'duplicate'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Custom alias already taken')
