from flask import Blueprint, render_template, current_app, flash, redirect, url_for, request
from flask_login import login_required, current_user
from bson import ObjectId
from datetime import datetime

extracurricular = Blueprint('extracurricular', __name__)

@extracurricular.route('/extracurricular')
def extracurricular_page():
    """Display all extracurricular activities."""
    activities = list(current_app.db.extracurricular.find().sort('start_date', -1))
    return render_template('extracurricular/extracurricular.html', title='Extracurricular Activities', activities=activities)

@extracurricular.route('/extracurricular/add', methods=['GET', 'POST'])
@login_required
def add_activity():
    """Add a new extracurricular activity."""
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        activity_data = {
            'title': request.form.get('title'),
            'organization': request.form.get('organization'),
            'description': request.form.get('description'),
            'start_date': request.form.get('start_date'),
            'end_date': request.form.get('end_date') if request.form.get('end_date') else 'Present',
            'skills': request.form.get('skills').split(',') if request.form.get('skills') else [],
            'created_at': datetime.utcnow()
        }
        
        current_app.db.extracurricular.insert_one(activity_data)
        flash('Extracurricular activity added successfully!', 'success')
        return redirect(url_for('extracurricular.extracurricular_page'))
    
    return render_template('extracurricular/add_activity.html', title='Add Extracurricular Activity')

@extracurricular.route('/extracurricular/edit/<activity_id>', methods=['GET', 'POST'])
@login_required
def edit_activity(activity_id):
    """Edit an existing extracurricular activity."""
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))
    
    activity = current_app.db.extracurricular.find_one({'_id': ObjectId(activity_id)})
    if not activity:
        flash('Activity not found.', 'danger')
        return redirect(url_for('extracurricular.extracurricular_page'))
    
    if request.method == 'POST':
        updated_data = {
            'title': request.form.get('title'),
            'organization': request.form.get('organization'),
            'description': request.form.get('description'),
            'start_date': request.form.get('start_date'),
            'end_date': request.form.get('end_date') if request.form.get('end_date') else 'Present',
            'skills': request.form.get('skills').split(',') if request.form.get('skills') else [],
            'updated_at': datetime.utcnow()
        }
        
        current_app.db.extracurricular.update_one(
            {'_id': ObjectId(activity_id)},
            {'$set': updated_data}
        )
        
        flash('Extracurricular activity updated successfully!', 'success')
        return redirect(url_for('extracurricular.extracurricular_page'))
    
    return render_template('extracurricular/edit_activity.html', title='Edit Extracurricular Activity', activity=activity)

@extracurricular.route('/extracurricular/delete/<activity_id>', methods=['POST'])
@login_required
def delete_activity(activity_id):
    """Delete an extracurricular activity."""
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))
    
    result = current_app.db.extracurricular.delete_one({'_id': ObjectId(activity_id)})
    
    if result.deleted_count > 0:
        flash('Extracurricular activity deleted successfully!', 'success')
    else:
        flash('Activity not found.', 'danger')
    
    return redirect(url_for('extracurricular.extracurricular_page')) 