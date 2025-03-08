from flask import Blueprint, render_template, current_app
from bson.objectid import ObjectId

projects = Blueprint('projects', __name__)

@projects.route('/projects')
def projects_page():
    projects_list = list(current_app.db.projects.find().sort('created_at', -1))
    return render_template('projects/projects.html', title='Projects', projects=projects_list)

@projects.route('/projects/<project_id>')
def project_detail(project_id):
    project = current_app.db.projects.find_one({'_id': ObjectId(project_id)})
    if not project:
        return render_template('errors/404.html'), 404
    
    return render_template('projects/project_detail.html', title=project['title'], project=project) 