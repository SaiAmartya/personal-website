from flask_login import UserMixin
from bson.objectid import ObjectId

class User(UserMixin):
    def __init__(self, user_data):
        self._id = user_data.get('_id')
        self.id = str(self._id) if self._id else None
        self.username = user_data.get('username')
        self.email = user_data.get('email')
        self.is_admin = user_data.get('is_admin', False)
    
    def get_id(self):
        return self.id
        
    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, is_admin={self.is_admin})" 