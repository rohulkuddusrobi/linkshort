I want to build an advanced URL Shortener web app using Python and Django.

### 🔧 Technologies to use:
- Python (main language)
- Django (web framework)
- HTML, CSS, JavaScript (for frontend)
- Django Template Engine for views
- MySQL xampp server (port 3307
)
- qrcode Python library (for optional QR code feature)

### 📁 Project Structure:
- Use Django standard project layout:
  - One app named `shortener`
  - Templates and static folders included
  - Home page for shortening URL
  - Redirection handler view

### ✅ Features to implement:

1. **URL Shortening System**
   - Input long URL from user
   - Generate short unique code using base62 encoding or random hash
   - Store long URL, short code, creation date, expiry (optional), and click count in database

2. **Redirection View**
   - When user visits `/<short-code>`, redirect to original long URL
   - Increase click count

3. **Click Tracker**
   - Track how many times each short link is clicked
   - Store timestamp of each visit (optional)

4. **Optional: Custom Alias**
   - Allow users to input custom short URL (if not taken)

5. **Optional: Expiry Time**
   - Allow link to expire after a certain date
   - Show error if link expired

6. **Admin Panel**
   - Use Django admin to manage all shortened links

7. **Frontend**
   - Clean responsive UI with form to input URL
   - Display short link after creation
   - Copy to clipboard button
   - Error messages if URL is invalid or custom alias is taken

8. **(Optional Bonus) QR Code Generator**
   - Use Python `qrcode` library
   - Generate downloadable QR code for each short URL

### 📦 Models to Create:
- `ShortURL`
  - id (auto)
  - original_url (TextField)
  - short_code (CharField, unique)
  - created_at (DateTime)
  - expires_at (DateTime, optional)
  - click_count (Integer)
  - custom_alias (CharField, optional)

### 🌐 Routes:
- `/` → Home page (shorten form)
- `/<short_code>/` → Redirection view
- `/admin/` → Django admin

### 🔐 Auth (optional):
- Use Django default user system to allow user login
- Users can view their own shortened links

### 🎯 Target:
- Make the app fully functional locally using SQLite
- Make it deployable on PythonAnywhere or Render later

