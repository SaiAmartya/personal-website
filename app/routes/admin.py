from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session, jsonify
from flask_login import login_required, current_user
from app.forms import ProjectForm, AccomplishmentForm, BlogPostForm
from app.models.content import Project, Accomplishment, BlogPost
from app.utils import save_image
from bson.objectid import ObjectId
from datetime import datetime, date
import logging
from functools import wraps

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Add a custom admin_required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f"Admin check in decorator - current_user: {current_user}")
        print(f"Admin check in decorator - is_authenticated: {current_user.is_authenticated}, is_admin: {getattr(current_user, 'is_admin', False)}")
        
        if not current_user.is_authenticated:
            print("User is not authenticated, redirecting to login")
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('auth.login', next=request.url))
            
        if not getattr(current_user, 'is_admin', False):
            print("User is not admin, redirecting to home")
            flash('You do not have permission to access this page', 'danger')
            return redirect(url_for('main.home'))
            
        print("User is admin, proceeding to view")
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
@admin.route('/dashboard')
@admin_required
def dashboard():
    # Count items in each collection
    project_count = current_app.db.projects.count_documents({})
    accomplishment_count = current_app.db.accomplishments.count_documents({})
    blog_count = current_app.db.blog_posts.count_documents({})
    message_count = current_app.db.contact_messages.count_documents({})
    
    # Get recent messages
    recent_messages = list(current_app.db.contact_messages.find().sort('created_at', -1).limit(5))
    
    return render_template('admin/dashboard.html', 
                          title='Admin Dashboard',
                          project_count=project_count,
                          accomplishment_count=accomplishment_count,
                          blog_count=blog_count,
                          message_count=message_count,
                          recent_messages=recent_messages)

# Project routes
@admin.route('/projects')
@admin_required
def projects():
    # Sort by display_order first, then by created_at as a fallback
    projects = list(current_app.db.projects.find().sort([('display_order', 1), ('created_at', -1)]))
    return render_template('admin/projects.html', title='Manage Projects', projects=projects)

@admin.route('/projects/new', methods=['GET', 'POST'])
@admin_required
def new_project():
    form = ProjectForm()
    
    if request.method == 'POST':
        print("Form submitted with data:", request.form)
        
    if form.validate_on_submit():
        project = Project()
        project.title = form.title.data
        project.brief_description = form.brief_description.data
        project.description = form.description.data
        project.link = form.link.data
        project.technologies = [tech.strip() for tech in form.technologies.data.split(',') if tech.strip()]
        project.created_at = datetime.now()
        
        if form.image.data:
            project.image_url = save_image(form.image.data, 'images/projects')
        
        current_app.db.projects.insert_one(project.to_dict())
        flash('Project created successfully!', 'success')
        return redirect(url_for('admin.projects'))
    elif request.method == 'POST':
        print("Form validation errors:", form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'danger')
    
    return render_template('admin/project_form.html', title='New Project', form=form, legend='New Project')

@admin.route('/projects/<project_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_project(project_id):
    project_data = current_app.db.projects.find_one({'_id': ObjectId(project_id)})
    if not project_data:
        flash('Project not found', 'danger')
        return redirect(url_for('admin.projects'))
    
    project = Project(project_data)
    form = ProjectForm()
    
    if form.validate_on_submit():
        update_data = {
            'title': form.title.data,
            'brief_description': form.brief_description.data,
            'description': form.description.data,
            'link': form.link.data,
            'technologies': [tech.strip() for tech in form.technologies.data.split(',') if tech.strip()]
        }
        
        if form.image.data:
            update_data['image_url'] = save_image(form.image.data, 'images/projects')
        
        current_app.db.projects.update_one({'_id': ObjectId(project_id)}, {'$set': update_data})
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    if request.method == 'GET':
        form.title.data = project.title
        form.brief_description.data = project.brief_description
        form.description.data = project.description
        form.link.data = project.link
        form.technologies.data = ', '.join(project.technologies)
    
    return render_template('admin/project_form.html', title='Edit Project', form=form, legend='Edit Project', project=project)

@admin.route('/projects/<project_id>/delete', methods=['POST'])
@admin_required
def delete_project(project_id):
    current_app.db.projects.delete_one({'_id': ObjectId(project_id)})
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.projects'))

@admin.route('/projects/update-order', methods=['POST'])
@admin_required
def update_project_order():
    try:
        data = request.json
        projects = data.get('projects', [])
        
        # Update each project with its new display order
        for project in projects:
            project_id = project.get('id')
            order = project.get('order')
            
            if project_id and order is not None:
                current_app.db.projects.update_one(
                    {'_id': ObjectId(project_id)},
                    {'$set': {'display_order': order}}
                )
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error updating project order: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

# Accomplishment routes
@admin.route('/accomplishments')
@admin_required
def accomplishments():
    # Sort by display_order first, then by date as a fallback
    accomplishments = list(current_app.db.accomplishments.find().sort([('display_order', 1), ('date', -1)]))
    return render_template('admin/accomplishments.html', title='Manage Accomplishments', accomplishments=accomplishments)

@admin.route('/accomplishments/new', methods=['GET', 'POST'])
@admin_required
def new_accomplishment():
    form = AccomplishmentForm()
    if form.validate_on_submit():
        accomplishment = Accomplishment()
        accomplishment.title = form.title.data
        accomplishment.brief_description = form.brief_description.data
        accomplishment.description = form.description.data
        
        # Convert date to datetime if it's a date object
        date_value = form.date.data
        if isinstance(date_value, date) and not isinstance(date_value, datetime):
            # Convert to datetime at midnight
            date_value = datetime.combine(date_value, datetime.min.time())
        accomplishment.date = date_value
        
        accomplishment.category = form.category.data
        accomplishment.created_at = datetime.now()
        
        if form.image.data:
            accomplishment.image_url = save_image(form.image.data, 'images/accomplishments')
        
        current_app.db.accomplishments.insert_one(accomplishment.to_dict())
        flash('Accomplishment created successfully!', 'success')
        return redirect(url_for('admin.accomplishments'))
    
    return render_template('admin/accomplishment_form.html', title='New Accomplishment', form=form, legend='New Accomplishment')

@admin.route('/accomplishments/<accomplishment_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_accomplishment(accomplishment_id):
    accomplishment_data = current_app.db.accomplishments.find_one({'_id': ObjectId(accomplishment_id)})
    if not accomplishment_data:
        flash('Accomplishment not found', 'danger')
        return redirect(url_for('admin.accomplishments'))
    
    accomplishment = Accomplishment(accomplishment_data)
    form = AccomplishmentForm()
    
    if form.validate_on_submit():
        # Convert date to datetime if it's a date object
        date_value = form.date.data
        if isinstance(date_value, date) and not isinstance(date_value, datetime):
            # Convert to datetime at midnight
            date_value = datetime.combine(date_value, datetime.min.time())
            
        update_data = {
            'title': form.title.data,
            'brief_description': form.brief_description.data,
            'description': form.description.data,
            'date': date_value,
            'category': form.category.data
        }
        
        if form.image.data:
            update_data['image_url'] = save_image(form.image.data, 'images/accomplishments')
        
        current_app.db.accomplishments.update_one({'_id': ObjectId(accomplishment_id)}, {'$set': update_data})
        flash('Accomplishment updated successfully!', 'success')
        return redirect(url_for('admin.accomplishments'))
    
    if request.method == 'GET':
        form.title.data = accomplishment.title
        form.brief_description.data = accomplishment.brief_description
        form.description.data = accomplishment.description
        form.date.data = accomplishment.date
        form.category.data = accomplishment.category
    
    return render_template('admin/accomplishment_form.html', title='Edit Accomplishment', form=form, legend='Edit Accomplishment', accomplishment=accomplishment)

@admin.route('/accomplishments/<accomplishment_id>/delete', methods=['POST'])
@admin_required
def delete_accomplishment(accomplishment_id):
    current_app.db.accomplishments.delete_one({'_id': ObjectId(accomplishment_id)})
    flash('Accomplishment deleted successfully!', 'success')
    return redirect(url_for('admin.accomplishments'))

@admin.route('/accomplishments/update-order', methods=['POST'])
@admin_required
def update_accomplishment_order():
    try:
        data = request.json
        accomplishments = data.get('accomplishments', [])
        
        # Update each accomplishment with its new display order
        for accomplishment in accomplishments:
            accomplishment_id = accomplishment.get('id')
            order = accomplishment.get('order')
            
            if accomplishment_id and order is not None:
                current_app.db.accomplishments.update_one(
                    {'_id': ObjectId(accomplishment_id)},
                    {'$set': {'display_order': order}}
                )
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error updating accomplishment order: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

# Blog routes
@admin.route('/blog')
@admin_required
def blog_posts():
    # Sort by display_order first, then by created_at as a fallback
    blog_posts = list(current_app.db.blog_posts.find().sort([('display_order', 1), ('created_at', -1)]))
    return render_template('admin/blog_posts.html', title='Manage Blog Posts', blog_posts=blog_posts)

@admin.route('/blog/new', methods=['GET', 'POST'])
@admin_required
def new_blog_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        post = BlogPost()
        post.title = form.title.data
        post.brief_description = form.brief_description.data
        post.content = form.content.data
        post.tags = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
        post.created_at = datetime.now()
        post.updated_at = datetime.now()
        
        if form.image.data:
            post.image_url = save_image(form.image.data, 'images/blog')
        
        current_app.db.blog_posts.insert_one(post.to_dict())
        flash('Blog post created successfully!', 'success')
        return redirect(url_for('admin.blog_posts'))
    
    return render_template('admin/blog_form.html', title='New Blog Post', form=form, legend='New Blog Post')

@admin.route('/blog/<post_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_blog_post(post_id):
    post_data = current_app.db.blog_posts.find_one({'_id': ObjectId(post_id)})
    if not post_data:
        flash('Blog post not found', 'danger')
        return redirect(url_for('admin.blog_posts'))
    
    post = BlogPost(post_data)
    form = BlogPostForm()
    
    if form.validate_on_submit():
        update_data = {
            'title': form.title.data,
            'brief_description': form.brief_description.data,
            'content': form.content.data,
            'tags': [tag.strip() for tag in form.tags.data.split(',') if tag.strip()],
            'updated_at': datetime.now()
        }
        
        if form.image.data:
            update_data['image_url'] = save_image(form.image.data, 'images/blog')
        
        current_app.db.blog_posts.update_one({'_id': ObjectId(post_id)}, {'$set': update_data})
        flash('Blog post updated successfully!', 'success')
        return redirect(url_for('admin.blog_posts'))
    
    if request.method == 'GET':
        form.title.data = post.title
        form.brief_description.data = post.brief_description
        form.content.data = post.content
        form.tags.data = ', '.join(post.tags)
    
    return render_template('admin/blog_form.html', title='Edit Blog Post', form=form, legend='Edit Blog Post', post=post)

@admin.route('/blog/<post_id>/delete', methods=['POST'])
@admin_required
def delete_blog_post(post_id):
    current_app.db.blog_posts.delete_one({'_id': ObjectId(post_id)})
    flash('Blog post deleted successfully!', 'success')
    return redirect(url_for('admin.blog_posts'))

@admin.route('/blog/update-order', methods=['POST'])
@admin_required
def update_blog_post_order():
    try:
        data = request.json
        blog_posts = data.get('blog_posts', [])
        
        # Update each blog post with its new display order
        for post in blog_posts:
            post_id = post.get('id')
            order = post.get('order')
            
            if post_id and order is not None:
                current_app.db.blog_posts.update_one(
                    {'_id': ObjectId(post_id)},
                    {'$set': {'display_order': order}}
                )
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error updating blog post order: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

# Messages
@admin.route('/messages')
@admin_required
def messages():
    messages = list(current_app.db.contact_messages.find().sort('created_at', -1))
    return render_template('admin/messages.html', title='Contact Messages', messages=messages)

@admin.route('/messages/<message_id>/delete', methods=['POST'])
@admin_required
def delete_message(message_id):
    current_app.db.contact_messages.delete_one({'_id': ObjectId(message_id)})
    flash('Message deleted successfully!', 'success')
    return redirect(url_for('admin.messages'))

@admin.route('/profile-image', methods=['GET', 'POST'])
@admin_required
def profile_image():
    current_image = current_app.db.site_settings.find_one({"setting_name": "profile_image"})
    profile_image = current_image.get("value") if current_image else None
    
    if request.method == 'POST':
        if 'profile_image' in request.files and request.files['profile_image'].filename:
            # Save the new image
            image_path = save_image(request.files['profile_image'], 'profile')
            
            # Update or insert the profile image setting
            current_app.db.site_settings.update_one(
                {"setting_name": "profile_image"},
                {"$set": {"value": image_path, "updated_at": datetime.utcnow()}},
                upsert=True
            )
            
            flash('Profile image updated successfully!', 'success')
            return redirect(url_for('admin.profile_image'))
        
        elif 'remove_image' in request.form:
            # Remove the profile image setting
            current_app.db.site_settings.delete_one({"setting_name": "profile_image"})
            flash('Profile image removed successfully!', 'success')
            return redirect(url_for('admin.profile_image'))
    
    return render_template('admin/profile_image.html', 
                          title='Manage Profile Image',
                          profile_image=profile_image)

# Extracurricular Activities
@admin.route('/activities')
@admin_required
def activities():
    # Sort by display_order first, then by start_date as a fallback
    activities = list(current_app.db.extracurricular.find().sort([('display_order', 1), ('start_date', -1)]))
    return render_template('admin/activities.html', title='Manage Activities', activities=activities)

@admin.route('/activities/update-order', methods=['POST'])
@admin_required
def update_activity_order():
    try:
        data = request.json
        activities = data.get('activities', [])
        
        # Update each activity with its new display order
        for activity in activities:
            activity_id = activity.get('id')
            order = activity.get('order')
            
            if activity_id and order is not None:
                current_app.db.extracurricular.update_one(
                    {'_id': ObjectId(activity_id)},
                    {'$set': {'display_order': order}}
                )
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error updating activity order: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}) 