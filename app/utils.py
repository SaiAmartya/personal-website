import os
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app, url_for
from PIL import Image
from datetime import datetime
import cloudinary
import cloudinary.uploader

def save_image(form_image, folder='uploads'):
    """Save uploaded image and return the filename"""
    # Check if we're running on Vercel (production)
    if os.getenv('VERCEL_ENV') or os.getenv('VERCEL'):
        try:
            # Configure Cloudinary if not already configured
            if not hasattr(current_app, 'cloudinary_configured'):
                cloudinary.config(
                    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
                    api_key=os.getenv('CLOUDINARY_API_KEY'),
                    api_secret=os.getenv('CLOUDINARY_API_SECRET')
                )
                current_app.cloudinary_configured = True
            
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                form_image,
                folder=folder,
                resource_type="auto"
            )
            
            # Return the secure URL from Cloudinary
            return upload_result['secure_url']
        except Exception as e:
            print(f"Cloudinary upload error: {e}")
            # Fall back to local storage if Cloudinary fails
            pass
    
    # Local storage for development environment
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_image.filename)
    image_filename = random_hex + file_ext
    
    # Create directory if it doesn't exist
    upload_dir = os.path.join(current_app.root_path, 'static', folder)
    os.makedirs(upload_dir, exist_ok=True)
    
    image_path = os.path.join(upload_dir, image_filename)
    
    # Resize image to optimize storage and loading
    output_size = (1200, 1200)
    img = Image.open(form_image)
    img.thumbnail(output_size)
    img.save(image_path)
    
    return os.path.join(folder, image_filename)

def send_email(to_email, subject, body):
    """Send email using SMTP"""
    sender_email = os.getenv('EMAIL_USER')
    sender_password = os.getenv('EMAIL_PASSWORD')
    
    if not sender_email or not sender_password:
        # Log error and return if credentials are missing
        print("Email credentials not configured")
        return False
    
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject
    
    message.attach(MIMEText(body, 'html'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def format_date(date):
    """Format date for display"""
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return date
    
    return date.strftime('%B %d, %Y')

def get_image_url(image_path):
    """
    Helper function to get the correct image URL whether it's stored locally or on Cloudinary
    """
    if not image_path:
        return None
        
    # Check if it's a Cloudinary URL (starts with http or https)
    if image_path.startswith('http://') or image_path.startswith('https://'):
        return image_path
    
    # Otherwise, it's a local path, so use url_for
    return url_for('static', filename=image_path) 