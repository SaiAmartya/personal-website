from flask import Blueprint, render_template, current_app

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    # Get recent projects, accomplishments, and blog posts
    projects = list(current_app.db.projects.find().sort('created_at', -1).limit(3))
    accomplishments = list(current_app.db.accomplishments.find().sort('date', -1).limit(3))
    blog_posts = list(current_app.db.blog_posts.find().sort('created_at', -1).limit(3))
    
    return render_template('home.html', 
                          title='Home',
                          projects=projects,
                          accomplishments=accomplishments,
                          blog_posts=blog_posts) 