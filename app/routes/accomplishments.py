from flask import Blueprint, render_template, current_app, request
from bson.objectid import ObjectId

accomplishments = Blueprint('accomplishments', __name__)

@accomplishments.route('/accomplishments')
def accomplishments_page():
    # Get filter category if provided
    category = request.args.get('category')
    
    # Build query
    query = {}
    if category and category != 'all':
        query['category'] = category
    
    # Get accomplishments
    accomplishments_list = list(current_app.db.accomplishments.find(query).sort('date', -1))
    
    # Get all categories for filter
    categories = current_app.db.accomplishments.distinct('category')
    
    return render_template('accomplishments/accomplishments.html', 
                          title='Accomplishments', 
                          accomplishments=accomplishments_list,
                          categories=categories,
                          selected_category=category or 'all')

@accomplishments.route('/accomplishments/<accomplishment_id>')
def accomplishment_detail(accomplishment_id):
    accomplishment = current_app.db.accomplishments.find_one({'_id': ObjectId(accomplishment_id)})
    if not accomplishment:
        return render_template('errors/404.html'), 404
    
    return render_template('accomplishments/accomplishment_detail.html', 
                          title=accomplishment['title'], 
                          accomplishment=accomplishment) 