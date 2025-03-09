import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Cloudinary
def config_cloudinary():
    cloudinary.config(
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET')
    )

def upload_image(file):
    """Upload an image to Cloudinary and return the URL"""
    if not file:
        return None
    
    try:
        # Upload the image to Cloudinary
        upload_result = cloudinary.uploader.upload(file)
        
        # Return the secure URL of the uploaded image
        return upload_result.get('secure_url')
    except Exception as e:
        print(f"Error uploading to Cloudinary: {e}")
        return None 