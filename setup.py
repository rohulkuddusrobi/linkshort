#!/usr/bin/env python3
"""
URL Shortener Setup Script
This script helps set up the URL Shortener Django project
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        if platform.system() == "Windows":
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command.split(), check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"   {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("   Please upgrade to Python 3.8 or higher")
        return False

def install_dependencies():
    """Install required Python packages"""
    packages = [
        "Django==4.2.7",
        "pymysql",
        "qrcode[pil]",
    ]
    
    for package in packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            return False
    return True

def setup_database():
    """Set up the database"""
    commands = [
        ("python manage.py makemigrations", "Creating migrations"),
        ("python manage.py makemigrations shortener", "Creating shortener app migrations"),
        ("python manage.py migrate", "Applying database migrations"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def create_superuser():
    """Prompt to create superuser"""
    response = input("\n🔐 Would you like to create a superuser account? (y/n): ")
    if response.lower() in ['y', 'yes']:
        print("Please follow the prompts to create your admin account:")
        try:
            subprocess.run("python manage.py createsuperuser", shell=True, check=True)
            print("✅ Superuser created successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to create superuser")

def main():
    """Main setup function"""
    print("🚀 URL Shortener Django Project Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    print("\n📦 Installing Dependencies...")
    if not install_dependencies():
        print("❌ Failed to install dependencies. Please check your internet connection and try again.")
        sys.exit(1)
    
    # Setup database
    print("\n🗄️ Setting up Database...")
    if not setup_database():
        print("❌ Failed to setup database. Please check for errors above.")
        sys.exit(1)
    
    # Create superuser
    create_superuser()
    
    # Success message
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Run: python manage.py runserver")
    print("2. Open: http://127.0.0.1:8000")
    print("3. Admin: http://127.0.0.1:8000/admin")
    print("\n🔧 Features:")
    print("• Shorten URLs with custom aliases")
    print("• Generate QR codes for links")
    print("• Track click analytics")
    print("• User dashboard and authentication")
    print("• Admin panel for management")
    print("\n📚 Check README.md for detailed documentation")
    print("=" * 50)

if __name__ == "__main__":
    main()
