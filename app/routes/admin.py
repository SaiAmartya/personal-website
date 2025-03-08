from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.forms import ProjectForm, AccomplishmentForm, BlogPostForm
from app.models.content import Project, Accomplishment, BlogPost
from app.utils import save_image
from bson.objectid import ObjectId
from datetime import datetime

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.before_request
def check_admin():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash('You do not have permission to access this page', 'danger')
        return redirect(url_for('main.home'))

@admin.route('/')
@admin.route('/dashboard')
@login_required
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
@login_required
def projects():
    projects = list(current_app.db.projects.find().sort('created_at', -1))
    return render_template('admin/projects.html', title='Manage Projects', projects=projects)

@admin.route('/projects/new', methods=['GET', 'POST'])
@login_required
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project()
        project.title = form.title.data
        project.description = form.description.data
        project.link = form.link.data
        project.technologies = [tech.strip() for tech in form.technologies.data.split(',') if tech.strip()]
        project.created_at = datetime.now()
        
        if form.image.data:
            project.image_url = save_image(form.image.data, 'images/projects')
        
        current_app.db.projects.insert_one(project.to_dict())
        flash('Project created successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    return render_template('admin/project_form.html', title='New Project', form=form, legend='New Project')

@admin.route('/projects/<project_id>/edit', methods=['GET', 'POST'])
@login_required
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
        form.description.data = project.description
        form.link.data = project.link
        form.technologies.data = ', '.join(project.technologies)
    
    return render_template('admin/project_form.html', title='Edit Project', form=form, legend='Edit Project', project=project)

@admin.route('/projects/<project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    current_app.db.projects.delete_one({'_id': ObjectId(project_id)})
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.projects'))

# Accomplishment routes
@admin.route('/accomplishments')
@login_required
def accomplishments():
    accomplishments = list(current_app.db.accomplishments.find().sort('date', -1))
    return render_template('admin/accomplishments.html', title='Manage Accomplishments', accomplishments=accomplishments)

@admin.route('/accomplishments/new', methods=['GET', 'POST'])
@login_required
def new_accomplishment():
    form = AccomplishmentForm()
    if form.validate_on_submit():
        accomplishment = Accomplishment()
        accomplishment.title = form.title.data
        accomplishment.description = form.description.data
        accomplishment.date = form.date.data
        accomplishment.category = form.category.data
        accomplishment.created_at = datetime.now()
        
        if form.image.data:
            accomplishment.image_url = save_image(form.image.data, 'images/accomplishments')
        
        current_app.db.accomplishments.insert_one(accomplishment.to_dict())
        flash('Accomplishment created successfully!', 'success')
        return redirect(url_for('admin.accomplishments'))
    
    return render_template('admin/accomplishment_form.html', title='New Accomplishment', form=form, legend='New Accomplishment')

@admin.route('/accomplishments/<accomplishment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_accomplishment(accomplishment_id):
    accomplishment_data = current_app.db.accomplishments.find_one({'_id': ObjectId(accomplishment_id)})
    if not accomplishment_data:
        flash('Accomplishment not found', 'danger')
        return redirect(url_for('admin.accomplishments'))
    
    accomplishment = Accomplishment(accomplishment_data)
    form = AccomplishmentForm()
    
    if form.validate_on_submit():
        update_data = {
            'title': form.title.data,
            'description': form.description.data,
            'date': form.date.data,
            'category': form.category.data
        }
        
        if form.image.data:
            update_data['image_url'] = save_image(form.image.data, 'images/accomplishments')
        
        current_app.db.accomplishments.update_one({'_id': ObjectId(accomplishment_id)}, {'$set': update_data})
        flash('Accomplishment updated successfully!', 'success')
        return redirect(url_for('admin.accomplishments'))
    
    if request.method == 'GET':
        form.title.data = accomplishment.title
        form.description.data = accomplishment.description
        form.date.data = accomplishment.date if isinstance(accomplishment.date, datetime) else None
        form.category.data = accomplishment.category
    
    return render_template('admin/accomplishment_form.html', title='Edit Accomplishment', form=form, legend='Edit Accomplishment', accomplishment=accomplishment)

@admin.route('/accomplishments/<accomplishment_id>/delete', methods=['POST'])
@login_required
def delete_accomplishment(accomplishment_id):
    current_app.db.accomplishments.delete_one({'_id': ObjectId(accomplishment_id)})
    flash('Accomplishment deleted successfully!', 'success')
    return redirect(url_for('admin.accomplishments'))

# Blog routes
@admin.route('/blog')
@login_required
def blog_posts():
    blog_posts = list(current_app.db.blog_posts.find().sort('created_at', -1))
    return render_template('admin/blog_posts.html', title='Manage Blog Posts', blog_posts=blog_posts)

@admin.route('/blog/new', methods=['GET', 'POST'])
@login_required
def new_blog_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post = BlogPost()
        blog_post.title = form.title.data
        blog_post.content = form.content.data
        blog_post.tags = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
        blog_post.created_at = datetime.now()
        blog_post.updated_at = datetime.now()
        
        if form.image.data:
            blog_post.image_url = save_image(form.image.data, 'images/blog')
        
        current_app.db.blog_posts.insert_one(blog_post.to_dict())
        flash('Blog post created successfully!', 'success')
        return redirect(url_for('admin.blog_posts'))
    
    return render_template('admin/blog_form.html', title='New Blog Post', form=form, legend='New Blog Post')

@admin.route('/blog/<post_id>/edit', methods=['GET', 'POST'])
@login_required
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
        form.content.data = post.content
        form.tags.data = ', '.join(post.tags)
    
    return render_template('admin/blog_form.html', title='Edit Blog Post', form=form, legend='Edit Blog Post', post=post)

@admin.route('/blog/<post_id>/delete', methods=['POST'])
@login_required
def delete_blog_post(post_id):
    current_app.db.blog_posts.delete_one({'_id': ObjectId(post_id)})
    flash('Blog post deleted successfully!', 'success')
    return redirect(url_for('admin.blog_posts'))

# Messages
@admin.route('/messages')
@login_required
def messages():
    messages = list(current_app.db.contact_messages.find().sort('created_at', -1))
    return render_template('admin/messages.html', title='Contact Messages', messages=messages)

@admin.route('/messages/<message_id>/delete', methods=['POST'])
@login_required
def delete_message(message_id):
    current_app.db.contact_messages.delete_one({'_id': ObjectId(message_id)})
    flash('Message deleted successfully!', 'success')
    return redirect(url_for('admin.messages')) 