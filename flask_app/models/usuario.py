
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from datetime import datetime

class Usuario:
    def __init__(self ,data):
        self.id = data['id']
        self.name = data['name']
        self.alias = data['alias']
        self.email = data['email']
        self.password = data['password']
        self.birthday = data['birthday']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (name , alias, email, password, birthday, created_at) VALUES ( %(name)s , %(alias)s, %(email)s, %(password)s, %(birthday)s , NOW());"
        return connectToMySQL('mydb').query_db(query, data)
    
    @classmethod
    def find(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        return connectToMySQL('mydb').query_db(query, data)

    @classmethod
    def friendships(cls, data):
        query = 'SELECT users.id, users_2.id as friend_id, users_2.name as friend_name, users_2.alias as friend_alias, users_2.email as friend_email FROM users JOIN friendships ON users.id = friendships.user_id JOIN users as users_2 ON friendships.user2_id = users_2.id WHERE users.id = %(id)s' 
        return connectToMySQL('mydb').query_db(query, data)
    
    @classmethod
    def not_friendships(cls, data):
        query = 'SELECT * FROM users WHERE id NOT IN (SELECT friendships.user2_id FROM users JOIN friendships ON users.id = friendships.user_id WHERE users.id = %(id)s) AND users.id != %(id)s;'
        return connectToMySQL('mydb').query_db(query, data)
    
    @classmethod
    def find_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        return connectToMySQL('mydb').query_db(query, data)
    
    @classmethod
    def validate(cls, data):
        
        is_valid = True

        if len(data['password']) < 8:
            flash('Password needs to have at least 8 characters')
            is_valid = False
        
        name_regex = re.compile(r'^[a-zA-Z ]+$')
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        email = {'email': data['email']}
        if len(cls.find(email)) > 0:
            flash('This email has already been used for another account')
            is_valid = False

        if len(data['name']) < 2 or not name_regex.match(data['name']):
            flash('Name is not valid')
            is_valid = False
        
        if len(data['alias']) < 2:
            flash('Alias is not valid')
            is_valid = False
        
        if not email_regex.match(data['email']):
            flash('Email is not valid')
            is_valid = False

        if data['password'] != data['password_2']:
            flash('Passwords did not coincide')
            is_valid = False
        
        if data['birthday'] == '':
            flash('You need to enter a date of birth')
            is_valid = False

        if data['birthday'] != '': 
            inc = datetime.today() - datetime.strptime(data['birthday'], '%Y-%m-%d')
            print(inc.total_seconds()/(60*60*24*365.25))
        
            if inc.total_seconds()/(60*60*24*365.25) < 16:
                flash('You should be at least 16 years old to register')
                is_valid = False
        
        return is_valid