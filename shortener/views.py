from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from .models import ShortURL
import qrcode
from io import BytesIO
import base64

def home(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        custom_alias = request.POST.get('custom_alias', '').strip()
        expires_in_days = request.POST.get('expires_in_days')
        
        # Validate URL
        validator = URLValidator()
        try:
            validator(original_url)
        except ValidationError:
            messages.error(request, 'Please enter a valid URL')
            return render(request, 'shortener/home.html')
        
        # Check if custom alias is available
        if custom_alias:
            if ShortURL.objects.filter(custom_alias=custom_alias).exists():
                messages.error(request, 'Custom alias already taken')
                return render(request, 'shortener/home.html')
            short_code = custom_alias
        else:
            short_code = ShortURL.generate_short_code()
        
        # Set expiry date
        expires_at = None
        if expires_in_days:
            try:
                days = int(expires_in_days)
                expires_at = timezone.now() + timezone.timedelta(days=days)
            except ValueError:
                pass
        
        # Create short URL
        short_url = ShortURL.objects.create(
            original_url=original_url,
            short_code=short_code,
            custom_alias=custom_alias if custom_alias else None,
            expires_at=expires_at,
            user=request.user if request.user.is_authenticated else None
        )
        
        # Generate QR code
        qr_code_data = generate_qr_code(request.build_absolute_uri(reverse('redirect_url', args=[short_code])))
        
        context = {
            'short_url': short_url,
            'full_short_url': request.build_absolute_uri(reverse('redirect_url', args=[short_code])),
            'qr_code': qr_code_data,
        }
        return render(request, 'shortener/success.html', context)
    
    return render(request, 'shortener/home.html')

def redirect_url(request, short_code):
    short_url = get_object_or_404(ShortURL, short_code=short_code)
    
    # Check if expired
    if short_url.is_expired():
        return render(request, 'shortener/expired.html')
    
    # Increment click count
    short_url.click_count += 1
    short_url.save()
    
    return redirect(short_url.original_url)

def generate_qr_code(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Convert to base64 for embedding in HTML
    image_data = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{image_data}"

def download_qr(request, short_code):
    short_url = get_object_or_404(ShortURL, short_code=short_code)
    full_url = request.build_absolute_uri(reverse('redirect_url', args=[short_code]))
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(full_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{short_code}_qr.png"'
    return response

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'shortener/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'shortener/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def user_dashboard(request):
    urls = ShortURL.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(urls, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_urls': urls.count(),
        'total_clicks': sum(url.click_count for url in urls),
    }
    return render(request, 'shortener/dashboard.html', context)

@login_required
def delete_url(request, short_code):
    url = get_object_or_404(ShortURL, short_code=short_code, user=request.user)
    if request.method == 'POST':
        url.delete()
        messages.success(request, 'URL deleted successfully.')
    return redirect('dashboard')

def analytics(request, short_code):
    short_url = get_object_or_404(ShortURL, short_code=short_code)
    # Only show analytics to the owner or if no user is set
    if short_url.user and short_url.user != request.user:
        messages.error(request, 'You do not have permission to view these analytics.')
        return redirect('home')
    
    context = {
        'short_url': short_url,
        'full_short_url': request.build_absolute_uri(reverse('redirect_url', args=[short_code])),
    }
    return render(request, 'shortener/analytics.html', context)
