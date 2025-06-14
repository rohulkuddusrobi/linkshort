# URL Shortener - Advanced Django Web Application

A powerful and feature-rich URL shortener built with Django that provides comprehensive link management, analytics, and QR code generation capabilities.

## 🚀 Features

### Core Functionality
- **URL Shortening**: Convert long URLs into short, manageable links
- **Custom Aliases**: Create personalized short URLs with custom aliases
- **Link Expiration**: Set expiration dates for time-sensitive links
- **Click Tracking**: Monitor link performance with detailed click counts
- **QR Code Generation**: Automatic QR code creation for each shortened URL

### User Management
- **User Authentication**: Register, login, and manage your account
- **Personal Dashboard**: View and manage all your shortened URLs
- **Link Analytics**: Detailed statistics for each shortened URL
- **Link Management**: Delete unwanted links from your dashboard

### Advanced Features
- **Responsive Design**: Beautiful, mobile-friendly interface using Bootstrap 5
- **Admin Panel**: Comprehensive Django admin interface for link management
- **Bulk Operations**: Efficient handling of multiple URLs
- **Error Handling**: Graceful handling of expired and invalid links

## 🛠️ Technology Stack

- **Backend**: Python 3.13, Django 4.2.7
- **Database**: SQLite (easily configurable for MySQL/PostgreSQL)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Libraries**: 
  - QRCode for QR code generation
  - Pillow for image processing
  - PyMySQL for MySQL support

## 📁 Project Structure

```
urlshortener/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── db.sqlite3               # SQLite database
├── urlshortener/            # Main project settings
│   ├── settings.py          # Django configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI configuration
├── shortener/               # Main application
│   ├── models.py            # Database models
│   ├── views.py             # Application logic
│   ├── urls.py              # App URL routing
│   ├── admin.py             # Admin configuration
│   ├── templates/           # HTML templates
│   │   └── shortener/
│   │       ├── base.html    # Base template
│   │       ├── home.html    # Main shortening form
│   │       ├── success.html # Success page
│   │       ├── dashboard.html # User dashboard
│   │       ├── analytics.html # Link analytics
│   │       ├── login.html   # User login
│   │       ├── register.html # User registration
│   │       └── expired.html # Expired link page
│   └── templatetags/        # Custom template filters
└── static/                  # Static files (CSS, JS)
    └── css/
        └── style.css        # Custom styling
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository** (or download the project files)
   ```bash
   cd "c:\Users\TBC\OneDrive\Desktop\link shorter"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser** (for admin access)
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📖 Usage Guide

### Basic URL Shortening
1. Visit the homepage
2. Enter your long URL
3. Optionally add a custom alias
4. Set an expiration date (optional)
5. Click "Shorten URL"
6. Copy your shortened link and QR code

### User Account Features
1. **Register**: Create an account to track your links
2. **Dashboard**: View all your shortened URLs with statistics
3. **Analytics**: Click on any link to see detailed analytics
4. **Management**: Delete unwanted links from your dashboard

### Admin Features
- Access the Django admin panel at `/admin/`
- Manage all shortened URLs
- View user accounts and activity
- Monitor system-wide statistics

## 🔧 Configuration

### Database Configuration
By default, the project uses SQLite. To use MySQL:

1. Install MySQL server and create a database
2. Update `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'urlshortener_db',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

### Environment Variables
For production, consider using environment variables for sensitive settings:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False in production
- `DATABASE_URL`: Database connection string

## 🌐 API Endpoints

- `GET /` - Homepage with shortening form
- `POST /` - Create shortened URL
- `GET /<short_code>/` - Redirect to original URL
- `GET /dashboard/` - User dashboard (requires login)
- `GET /analytics/<short_code>/` - Link analytics
- `GET /qr/<short_code>/` - Download QR code
- `GET /login/` - User login
- `GET /register/` - User registration

## 🔒 Security Features

- CSRF protection on all forms
- User authentication and authorization
- URL validation to prevent malicious links
- Secure session management
- Admin panel protection

## 📊 Analytics & Tracking

Each shortened URL tracks:
- Total click count
- Creation date and time
- Expiration status
- User ownership (if logged in)
- Custom alias usage

## 🎨 UI/UX Features

- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Modern Interface**: Clean, intuitive design using Bootstrap 5
- **Interactive Elements**: Copy-to-clipboard functionality, form validation
- **Visual Feedback**: Success messages, error handling, loading states
- **Accessibility**: Proper ARIA labels and keyboard navigation

## 🚀 Deployment

### Local Development
The project is ready to run locally with the provided instructions.

### Production Deployment
For production deployment:

1. **Environment Setup**
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use a production database (PostgreSQL/MySQL)
   - Set up static file serving

2. **Platform Options**
   - **PythonAnywhere**: Excellent for Django apps
   - **Heroku**: Easy deployment with Git
   - **DigitalOcean**: VPS deployment
   - **AWS/GCP**: Cloud deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:
1. Check the Django debug output in the console
2. Verify all dependencies are installed
3. Ensure database migrations are applied
4. Check the Django documentation for troubleshooting

## 🔄 Future Enhancements

Potential features for future versions:
- Link preview generation
- Bulk URL import/export
- Advanced analytics dashboard
- Social media integration
- API for third-party integration
- Link password protection
- Geographic click tracking
- A/B testing for links

---

**Built with ❤️ using Django**

*This URL shortener provides enterprise-level features in an easy-to-use package, perfect for personal use, small businesses, or as a learning project for Django development.*
