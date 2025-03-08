import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm
from app.models.user import User
from bson.objectid import ObjectId
import time

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # If already logged in, redirect to dashboard
    if current_user.is_authenticated and getattr(current_user, 'is_admin', False):
        print(f"User already authenticated: {current_user}")
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        admin_password = os.getenv('ADMIN_PASSWORD')
        
        if form.password.data == admin_password:
            # Check if admin user exists
            admin_user = current_app.db.users.find_one({'is_admin': True})
            
            if not admin_user:
                # Create admin user if it doesn't exist
                user_id = current_app.db.users.insert_one({
                    'username': 'admin',
                    'email': os.getenv('EMAIL_USER'),
                    'is_admin': True,
                    'created_at': time.time()
                }).inserted_id
                
                admin_user = current_app.db.users.find_one({'_id': user_id})
                print(f"Created new admin user: {admin_user}")
            else:
                print(f"Found existing admin user: {admin_user}")
            
            # Ensure the admin flag is set
            if not admin_user.get('is_admin'):
                current_app.db.users.update_one(
                    {'_id': admin_user['_id']},
                    {'$set': {'is_admin': True}}
                )
                admin_user['is_admin'] = True
            
            # Create user object and login
            user = User(admin_user)
            
            # Make session permanent and set remember flag
            session.permanent = True
            login_success = login_user(user, remember=True)
            
            # Debug print to verify admin status
            print(f"User logged in: {user.username}, is_admin: {user.is_admin}, login success: {login_success}")
            print(f"User ID: {user.id}, type: {type(user.id)}")
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if next_page:
                print(f"Redirecting to next page: {next_page}")
            else:
                print(f"Redirecting to dashboard")
            
            return redirect(next_page if next_page else url_for('admin.dashboard'))
        else:
            flash('Login unsuccessful. Please check password', 'danger')
    
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.home')) 