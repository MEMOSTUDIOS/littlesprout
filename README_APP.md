# Little Sprout - Flask Application

## Overview
This Flask application serves the Little Sprout game website with backend functionality for email subscriptions and preorders.

## Setup Instructions

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

Or install Flask directly:
```bash
pip install Flask
```

### 2. Configure Email Settings (Optional)
Edit `app.py` and update the `EMAIL_CONFIG` dictionary:

```python
EMAIL_CONFIG = {
    'recipient_email': 'your-email@example.com',  # Where to receive notifications
    'sender_email': 'noreply@yourdomain.com',     # From address
    'smtp_server': 'smtp.gmail.com',              # Your SMTP server
    'smtp_port': 587,
    'smtp_username': 'your-email@gmail.com',      # SMTP username
    'smtp_password': 'your-app-password',         # SMTP password or app password
    'use_smtp': True  # Set to True to enable email sending
}
```

**Note:** If `use_smtp` is `False`, subscriptions will just be logged to the console.

### 3. Run the Application
```bash
python app.py
```

Or:
```bash
python3 app.py
```

The server will start on `http://127.0.0.1:5000` (localhost)

### 4. Access the Website
Open your browser and go to:
- http://localhost:5000
- http://127.0.0.1:5000

## Features

### Current Functionality
- ✅ Serves all static files (HTML, CSS, JS, images)
- ✅ Handles email subscription form submissions
- ✅ Validates email addresses
- ✅ Preorder form handling (demo mode)
- ✅ Email notifications (when SMTP is configured)

### API Endpoints

#### POST /subscribe
Handles email subscriptions.

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response (Success):**
```json
{
  "message": "Thank you for subscribing!"
}
```

#### POST /api/preorder
Handles preorder submissions (demo mode).

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "address": "123 Main St, City"
}
```

**Response (Success):**
```json
{
  "message": "Preorder confirmed! (Demo mode - no actual order placed)"
}
```

## Gmail SMTP Setup (If using Gmail)

If you want to use Gmail to send notification emails:

1. Enable 2-Factor Authentication on your Google Account
2. Generate an App Password:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the generated 16-character password
3. Update `app.py`:
   ```python
   'smtp_username': 'your-email@gmail.com',
   'smtp_password': 'your-16-char-app-password',
   'use_smtp': True
   ```

## Development Mode

The app runs in debug mode by default, which means:
- Auto-reloads on code changes
- Detailed error messages
- Not suitable for production use

## Production Deployment

For production, consider:
1. Set `debug=False` in `app.run()`
2. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```
3. Set up proper environment variables for sensitive data
4. Use a reverse proxy (nginx/Apache)

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, change it in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Email Not Sending
- Check SMTP credentials
- Verify firewall settings
- Check spam folder
- Enable "Less secure app access" or use App Passwords

### Static Files Not Loading
- Make sure all files are in the correct directory
- Check browser console for 404 errors
- Verify file paths in HTML match actual file locations

## File Structure
```
littlesprout/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── index.html          # Main page
├── en.html            # English version
├── game.html          # Game page
├── main.css           # Main stylesheet
├── assets/            # CSS, JS, fonts
│   ├── css/
│   ├── js/
│   └── sass/
└── images/            # Image assets
```

## Next Steps

You can extend this application by:
1. Adding a database to store subscriptions
2. Implementing user authentication
3. Creating an admin panel
4. Adding analytics
5. Implementing actual payment processing for preorders
6. Creating a newsletter system
7. Adding API for mobile app integration

## Support

For issues or questions, refer to:
- Flask documentation: https://flask.palletsprojects.com/
- Python SMTP library: https://docs.python.org/3/library/smtplib.html
