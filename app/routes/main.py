from flask import Blueprint, render_template, current_app

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    # Get all projects and activities for the carousels, but limit accomplishments and blog posts
    projects = list(current_app.db.projects.find().sort('created_at', -1))
    accomplishments = list(current_app.db.accomplishments.find().sort('date', -1).limit(3))
    blog_posts = list(current_app.db.blog_posts.find().sort('created_at', -1).limit(3))
    activities = list(current_app.db.extracurricular.find().sort('start_date', -1))
    
    # Get profile image if it exists
    site_settings = current_app.db.site_settings.find_one({"setting_name": "profile_image"})
    profile_image = site_settings.get("value") if site_settings else None
    
    # Print debug info
    print(f"Number of projects fetched for carousel: {len(projects)}")
    print(f"Number of activities fetched for carousel: {len(activities)}")
    print(f"Profile image: {profile_image}")
    
    return render_template('home.html', title='Home', 
                          projects=projects, 
                          accomplishments=accomplishments, 
                          blog_posts=blog_posts,
                          activities=activities,
                          profile_image=profile_image) 