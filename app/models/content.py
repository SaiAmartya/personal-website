from datetime import datetime, date

class Project:
    def __init__(self, project_data=None):
        if project_data is None:
            project_data = {}
        
        self.id = str(project_data.get('_id', ''))
        self.title = project_data.get('title', '')
        self.brief_description = project_data.get('brief_description', '')
        self.description = project_data.get('description', '')
        self.image_url = project_data.get('image_url', '')
        self.link = project_data.get('link', '')
        self.technologies = project_data.get('technologies', [])
        self.created_at = project_data.get('created_at', datetime.now())
    
    def to_dict(self):
        return {
            'title': self.title,
            'brief_description': self.brief_description,
            'description': self.description,
            'image_url': self.image_url,
            'link': self.link,
            'technologies': self.technologies,
            'created_at': self.created_at
        }

class Accomplishment:
    def __init__(self, accomplishment_data=None):
        if accomplishment_data is None:
            accomplishment_data = {}
        
        self.id = str(accomplishment_data.get('_id', ''))
        self.title = accomplishment_data.get('title', '')
        self.brief_description = accomplishment_data.get('brief_description', '')
        self.description = accomplishment_data.get('description', '')
        self.date = accomplishment_data.get('date', datetime.now())
        self.image_url = accomplishment_data.get('image_url', '')
        self.category = accomplishment_data.get('category', '')
        self.created_at = accomplishment_data.get('created_at', datetime.now())
    
    def to_dict(self):
        # Convert date to datetime if it's a date object
        date_value = self.date
        if isinstance(date_value, date) and not isinstance(date_value, datetime):
            # Convert to datetime at midnight
            date_value = datetime.combine(date_value, datetime.min.time())
        
        return {
            'title': self.title,
            'brief_description': self.brief_description,
            'description': self.description,
            'date': date_value,
            'image_url': self.image_url,
            'category': self.category,
            'created_at': self.created_at
        }

class BlogPost:
    def __init__(self, blog_data=None):
        if blog_data is None:
            blog_data = {}
        
        self.id = str(blog_data.get('_id', ''))
        self.title = blog_data.get('title', '')
        self.brief_description = blog_data.get('brief_description', '')
        self.content = blog_data.get('content', '')
        self.image_url = blog_data.get('image_url', '')
        self.tags = blog_data.get('tags', [])
        self.created_at = blog_data.get('created_at', datetime.now())
        self.updated_at = blog_data.get('updated_at', datetime.now())
    
    def to_dict(self):
        return {
            'title': self.title,
            'brief_description': self.brief_description,
            'content': self.content,
            'image_url': self.image_url,
            'tags': self.tags,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class ContactMessage:
    def __init__(self, message_data=None):
        if message_data is None:
            message_data = {}
        
        self.id = str(message_data.get('_id', ''))
        self.name = message_data.get('name', '')
        self.email = message_data.get('email', '')
        self.subject = message_data.get('subject', '')
        self.message = message_data.get('message', '')
        self.created_at = message_data.get('created_at', datetime.now())
    
    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'created_at': self.created_at
        } 