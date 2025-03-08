import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm
from app.models.user import User
from bson.objectid import ObjectId

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
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
                    'is_admin': True
                }).inserted_id
                
                admin_user = current_app.db.users.find_one({'_id': user_id})
            
            user = User(admin_user)
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('admin.dashboard'))
        else:
            flash('Login unsuccessful. Please check password', 'danger')
    
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home')) 