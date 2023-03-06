
from flask_app.config.mysqlconnection import connectToMySQL

class Amistad:
    def __init__(self ,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.friend_id = data['user2_id']
    
    @classmethod
    def add_friend(cls, data):
        query = "INSERT INTO friendships (user_id, user2_id) VALUES (%(user_id)s, %(friend_id)s), (%(friend_id)s, %(user_id)s);"
        return connectToMySQL('mydb').query_db(query, data)
    
    @classmethod
    def remove_friend(cls, data):
        query = "DELETE FROM friendships WHERE (user_id = %(user_id)s AND user2_id = %(friend_id)s) OR ((user2_id = %(user_id)s AND user_id = %(friend_id)s));"
        return connectToMySQL('mydb').query_db(query, data)