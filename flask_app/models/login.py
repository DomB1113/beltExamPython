from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import re

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                        # which is made by invoking the function Bcrypt with our app as an argument

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class Login:
    database ="sasquatch_schema"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod 
    def insert(cls,data):
        query = "INSERT INTO logins (first_name,last_name,email,password) VALUES (%(first_name)s , %(last_name)s , %(email)s , %(password)s) ;"
        return connectToMySQL(cls.database).query_db(query,data)

    @staticmethod
    def validate_registration(data):
        is_valid = True 
        query = "SELECT * FROM  logins WHERE email = %(email)s ;"
        results = connectToMySQL("sasquatch_schema").query_db(query,data)
        if len(results)>= 1:
            flash("Email is already taken", 'register')
            is_valid = False
        if len(data['first_name'])< 2:
            flash('First Name must be at least 2 letters', 'register')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Last Name must be at least 2 letters', 'register')
            is_valid = False
            is_valid = False
        if len(data['password']) < 8:
            flash('password needs to be 8 letters or more', 'register')
            is_valid = False 
        if data['password'] != data['confirm_password']:
            flash('Password must match', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email address')
            is_valid = False 
        return is_valid

    @classmethod 
    def get_by_email(cls,data):
        query = "SELECT * FROM logins WHERE email = %(email)s ;"
        results = connectToMySQL(cls.database).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod 
    def get_by_id(cls,data):
        query = "SELECT * FROM logins WHERE id = %(id)s ;"
        result = connectToMySQL(cls.database).query_db(query,data)
        return cls(result[0])
