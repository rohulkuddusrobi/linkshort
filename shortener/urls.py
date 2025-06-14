from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('analytics/<str:short_code>/', views.analytics, name='analytics'),
    path('delete/<str:short_code>/', views.delete_url, name='delete_url'),
    path('qr/<str:short_code>/', views.download_qr, name='download_qr'),
    path('<str:short_code>/', views.redirect_url, name='redirect_url'),
]
