from flask import Blueprint, render_template, current_app

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    # Get projects sorted by display_order (or created_at if display_order not set)
    projects = list(current_app.db.projects.find().sort([('display_order', 1), ('created_at', -1)]).limit(3))
    # Get accomplishments sorted by display_order (or date if display_order not set)
    accomplishments = list(current_app.db.accomplishments.find().sort([('display_order', 1), ('date', -1)]).limit(3))
    # Get blog posts sorted by display_order (or created_at if display_order not set)
    blog_posts = list(current_app.db.blog_posts.find().sort([('display_order', 1), ('created_at', -1)]).limit(3))
    # Get activities sorted by display_order (or start_date if display_order not set)
    activities = list(current_app.db.extracurricular.find().sort([('display_order', 1), ('start_date', -1)]).limit(3))
    
    # Get profile image if it exists
    site_settings = current_app.db.site_settings.find_one({"setting_name": "profile_image"})
    profile_image = site_settings.get("value") if site_settings else None
    
    # Print debug info
    print(f"Number of projects fetched: {len(projects)}")
    print(f"Number of activities fetched: {len(activities)}")
    print(f"Profile image: {profile_image}")
    
    return render_template('home.html', title='Home', 
                          projects=projects, 
                          accomplishments=accomplishments, 
                          blog_posts=blog_posts,
                          activities=activities,
                          profile_image=profile_image) 