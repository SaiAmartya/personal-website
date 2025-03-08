from flask import Blueprint, render_template, current_app, request
from bson.objectid import ObjectId

blog = Blueprint('blog', __name__)

@blog.route('/blog')
def blog_page():
    # Get tag filter if provided
    tag = request.args.get('tag')
    
    # Build query
    query = {}
    if tag:
        query['tags'] = tag
    
    # Get blog posts
    blog_posts = list(current_app.db.blog_posts.find(query).sort('created_at', -1))
    
    # Get all tags for filter
    all_tags = current_app.db.blog_posts.distinct('tags')
    
    return render_template('blog/blog.html', 
                          title='Blog', 
                          blog_posts=blog_posts,
                          tags=all_tags,
                          selected_tag=tag)

@blog.route('/blog/<post_id>')
def blog_post_detail(post_id):
    post = current_app.db.blog_posts.find_one({'_id': ObjectId(post_id)})
    if not post:
        return render_template('errors/404.html'), 404
    
    # Get related posts based on tags
    related_posts = []
    if post.get('tags'):
        related_posts = list(current_app.db.blog_posts.find({
            '_id': {'$ne': ObjectId(post_id)},
            'tags': {'$in': post['tags']}
        }).sort('created_at', -1).limit(3))
    
    return render_template('blog/blog_post.html', 
                          title=post['title'], 
                          post=post,
                          related_posts=related_posts) 