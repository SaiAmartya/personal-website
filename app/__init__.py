import os
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
    
    # Initialize MongoDB connection
    app.config['MONGODB_URI'] = os.getenv('MONGODB_URI')
    app.mongo_client = MongoClient(app.config['MONGODB_URI'])
    app.db = app.mongo_client.personal_site
    
    # Initialize extensions with app
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    bcrypt.init_app(app)
    
    # Import and register blueprints
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.admin import admin
    from app.routes.projects import projects
    from app.routes.accomplishments import accomplishments
    from app.routes.blog import blog
    from app.routes.contact import contact
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(projects)
    app.register_blueprint(accomplishments)
    app.register_blueprint(blog)
    app.register_blueprint(contact)
    
    # Import models
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        user_data = app.db.users.find_one({'_id': user_id})
        if user_data:
            return User(user_data)
        return None
    
    return app 