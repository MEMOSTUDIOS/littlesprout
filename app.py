"""
Little Sprout Flask Application
Serves the Little Sprout game website and handles email subscriptions
"""

from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from datetime import datetime
from pathlib import Path

app = Flask(__name__, 
            static_folder='.',
            static_url_path='')

# In-memory visitor tracking (will reset when server restarts)
visitors = []
visitor_count = 0

# In-memory card images tracking
card_images_cache = []
HIDDEN_CARDS_FOLDER = 'hidden-visual--cards'

# Configuration - Update these with your email settings
EMAIL_CONFIG = {
    'recipient_email': 'lucian.mangu@gmail.com',
    'sender_email': 'noreply@littlesprout.ro',
    'smtp_server': 'smtp.gmail.com',  # Update if using different email provider
    'smtp_port': 587,
    'smtp_username': '',  # Fill in for SMTP auth
    'smtp_password': '',  # Fill in for SMTP auth
    'use_smtp': False  # Set to True to enable email sending via SMTP
}

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def scan_card_images():
    """Scan the hidden-visual--cards folder and update the cache"""
    global card_images_cache
    folder_path = Path(HIDDEN_CARDS_FOLDER)
    
    if not folder_path.exists():
        card_images_cache = []
        return
    
    # Get all jpg files in the folder
    jpg_files = list(folder_path.glob('*.jpg'))
    
    # Create list of card data
    card_images_cache = []
    for jpg_file in jpg_files:
        # Remove .jpg extension and use filename as display name
        name = jpg_file.stem
        card_images_cache.append({
            'name': name.title(),  # Capitalize first letter of each word
            'filename': jpg_file.name,
            'path': f'{HIDDEN_CARDS_FOLDER}/{jpg_file.name}'
        })
    
    print(f"Loaded {len(card_images_cache)} card images from {HIDDEN_CARDS_FOLDER}")

def track_visitor():
    """Track visitor information"""
    global visitor_count, visitors
    
    visitor_count += 1
    
    # Get visitor information
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # Parse user agent for better device info
    device_info = user_agent
    if 'Mobile' in user_agent:
        device_info = 'Mobile - ' + user_agent.split('(')[1].split(')')[0] if '(' in user_agent else 'Mobile Device'
    elif 'Chrome' in user_agent:
        device_info = 'Chrome Browser'
    elif 'Firefox' in user_agent:
        device_info = 'Firefox Browser'
    elif 'Safari' in user_agent:
        device_info = 'Safari Browser'
    
    visitor_data = {
        'guest_number': visitor_count,
        'ip': ip,
        'device': device_info,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    visitors.append(visitor_data)
    
    # Keep only last 100 visitors
    if len(visitors) > 100:
        visitors.pop(0)

@app.route('/')
def index():
    """Serve the main page"""
    track_visitor()
    return send_from_directory('.', 'index.html')

@app.route('/dashboard')
def dashboard():
    """Serve the dashboard page"""
    return send_from_directory('.', 'dashboard.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (HTML, CSS, JS, images, etc.)"""
    if os.path.exists(path):
        return send_from_directory('.', path)
    return "File not found", 404

@app.route('/subscribe', methods=['POST'])
def subscribe():
    """Handle email subscription"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'email' not in data:
            return jsonify({
                'message': 'Error: Email address is required.'
            }), 400
        
        email = data.get('email', '').strip()
        
        # Validate email
        if not validate_email(email):
            return jsonify({
                'message': 'Error: A valid email address is required.'
            }), 400
        
        # Send notification email if SMTP is configured
        if EMAIL_CONFIG['use_smtp']:
            try:
                send_notification_email(email)
            except Exception as e:
                print(f"Error sending email: {str(e)}")
                return jsonify({
                    'message': 'Error: The server could not send the email. Please try again later.'
                }), 500
        else:
            # Log subscription to console if SMTP is not configured
            print(f"New subscription: {email}")
        
        return jsonify({
            'message': 'Thank you for subscribing!'
        }), 200
        
    except Exception as e:
        print(f"Subscription error: {str(e)}")
        return jsonify({
            'message': 'Error: An unexpected error occurred.'
        }), 500

def send_notification_email(subscriber_email):
    """Send email notification about new subscriber"""
    subject = "New Subscriber for Little Sprout!"
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_CONFIG['sender_email']
    msg['To'] = EMAIL_CONFIG['recipient_email']
    msg['Reply-To'] = subscriber_email
    msg['Subject'] = subject
    
    # Email body
    body = f"""A new user has subscribed to the Little Sprout mailing list.

Email Address: {subscriber_email}
"""
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Connect to SMTP server and send email
    with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
        server.starttls()
        if EMAIL_CONFIG['smtp_username'] and EMAIL_CONFIG['smtp_password']:
            server.login(EMAIL_CONFIG['smtp_username'], EMAIL_CONFIG['smtp_password'])
        server.send_message(msg)

@app.route('/api/preorder', methods=['POST'])
def preorder():
    """Handle preorder submissions (demo only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'address']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'message': f'Error: {field} is required.'
                }), 400
        
        # Validate email
        if not validate_email(data.get('email')):
            return jsonify({
                'message': 'Error: A valid email address is required.'
            }), 400
        
        # Log preorder (demo mode - no actual processing)
        print(f"Demo Preorder: {data.get('name')} ({data.get('email')})")
        
        return jsonify({
            'message': 'Preorder confirmed! (Demo mode - no actual order placed)'
        }), 200
        
    except Exception as e:
        print(f"Preorder error: {str(e)}")
        return jsonify({
            'message': 'Error: An unexpected error occurred.'
        }), 500

@app.route('/api/visitors', methods=['GET'])
def get_visitors():
    """Get list of visitors"""
    try:
        # Return visitors in reverse order (newest first)
        return jsonify({
            'visitors': list(reversed(visitors)),
            'total': visitor_count
        }), 200
    except Exception as e:
        print(f"Error fetching visitors: {str(e)}")
        return jsonify({
            'message': 'Error: Could not fetch visitors.'
        }), 500

@app.route('/api/card-images', methods=['GET'])
def get_card_images():
    """Get list of available card images, rescanning the folder"""
    try:
        # Rescan folder on every request
        scan_card_images()
        
        # Get search term if provided
        search_term = request.args.get('search', '').lower()
        
        if search_term:
            # Filter cards by search term
            filtered_cards = [
                card for card in card_images_cache
                if search_term in card['name'].lower()
            ]
            return jsonify({'cards': filtered_cards}), 200
        
        return jsonify({'cards': card_images_cache}), 200
    except Exception as e:
        print(f"Error fetching card images: {str(e)}")
        return jsonify({
            'message': 'Error: Could not fetch card images.',
            'cards': []
        }), 500

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return "Page not found", 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return "Internal server error", 500

if __name__ == '__main__':
    # Scan card images on startup
    scan_card_images()
    
    # Print startup information
    print("=" * 60)
    print("Little Sprout Server Starting...")
    print("=" * 60)
    print(f"Server will run on: http://127.0.0.1:5000")
    print(f"Email notifications: {'ENABLED' if EMAIL_CONFIG['use_smtp'] else 'DISABLED (logging to console)'}")
    print(f"Card images found: {len(card_images_cache)}")
    print("=" * 60)
    print("\nPress CTRL+C to stop the server\n")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
