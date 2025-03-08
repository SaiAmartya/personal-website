import os
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
from PIL import Image
from datetime import datetime

def save_image(form_image, folder='uploads'):
    """Save uploaded image and return the filename"""
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