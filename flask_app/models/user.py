from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe
from flask_app import DATABASE
import re

NAME_REGEX = re.compile(r'[a-zA-z]+')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users(first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result
        
        
    #get one user using the email
    @classmethod
    def get_one(cls,data):
        query = "SELECT * from users WHERE email = %(email)s"
        result = connectToMySQL(DATABASE).query_db(query,data)
        
        if len (result) > 0:
            return cls(result[0])
        else: 
            return None
    
    # TODO get all recipes 
    @classmethod
    def get_recipes(cls,data):
        query = "SELECT * FROM users LEFT JOIN recipes ON users.id = recipes.user_id WHERE users.id = %(id)s;"
        
        result = connectToMySQL(DATABASE).query_db(query,data)
        
        # validate if query returns anything
        if len(result) > 0:
            # set current recipe to result of query at index 0 -> which returns a list of dictionary
            current_user = cls(result[0])
            list_recipes = []
            # iterate through dictionary and decode it
            # add an instance of recipe to list
            for row in result:
                current_recipe = {
                    'id' : row['recipes.id'],
                    'name': row['name'],
                    'description': row['description'],
                    'instructions': row['instructions'],
                    'date_made': row['date_made'],
                    'under_thirty': row['under_thirty'],
                    'created_on': row['created_on'],
                    'updated_on': row['updated_on'],
                    'user_id': row['user_id'],
                }
                r = recipe.Recipe(current_recipe)
                list_recipes.append(r)
            current_user.list_recipes = list_recipes
            return current_user


    # validations
    @staticmethod
    def validate_login(data):
        is_valid = True
        if data['email'] == "":
            flash("Please provide your email.", "error_login_email")
            is_valid = False
        if data['password'] == "":
            flash("Please provide your email.", "error_password")
            is_valid = False
        return is_valid
        
    @staticmethod
    def validate_registration( data ):
        is_valid = True
        # first name validation
        if len(data['first_name']) < 2:
            flash("Name must be at least 2 characters", "error_reg")
            is_valid = False
        if not NAME_REGEX.match(data['first_name']):
            flash("Name must consist of only letters" , "error_reg")
            is_valid = False

        # last name validation
        if len(data['last_name']) < 2:
            flash("Name must be at least 2 characters", "error_reg")
            is_valid = False
        if not NAME_REGEX.match(data['last_name']):
            flash("Name must consist of only letters","error_reg")
            is_valid = False
        
        # email validation
        if data['email'] == "":
            flash("Email cannot be empty")
            is_valid = False    
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!","error_reg")
            is_valid = False
            
        # password validation 
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters","error_reg")
            is_valid = False
        if data['password'] != data['confirm_pass']:
            flash("Passwords must match!","error_reg")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_session():
        if 'id' in session:
            return True
        else:
            flash("You need to log in", "error_login")
            return False