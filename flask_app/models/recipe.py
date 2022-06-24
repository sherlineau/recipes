from flask import flash, session
from numpy import equal
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_thirty = data['under_thirty']
        self.created_on = data['created_on']
        self.updated_on = data['updated_on']
        self.user_id = data['user_id']
        
    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes(name,description,instructions,date_made,under_thirty,user_id) VALUES(%(name)s,%(description)s,%(instructions)s,%(date_made)s, %(under_thirty)s, %(user_id)s);"
        results = connectToMySQL(DATABASE).query_db(query,data)
        return results
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes"
        results = connectToMySQL(DATABASE).query_db(query)
        return results
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes where id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return (cls(result[0]))
    
    @classmethod
    def delete_one(cls,data):
        query = "DELETE FROM recipes where id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result
    
    @classmethod
    def update_one(cls,data):
        query = "UPDATE recipes SET name = %(name)s ,description = %(description)s,instructions = %(instructions)s, date_made = %(date_made)s,under_thirty = %(under_thirty)s WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result
    
    @staticmethod
    def validate_form(data):
        is_valid = True
        # name validation
        if len(data['name']) < 3:
            flash("Recipe name must be at least 3 characters",'error_recipe')
            is_valid = False
            
        # description validation
        if len(data['description']) < 3:
            flash("Description must be at least 3 characters",'error_recipe')
            is_valid = False
        
        # instruction validation
        if len(data['instructions']) < 3:
            flash("Instructions must be at least 3 characters",'error_recipe')
            is_valid = False
        
        # date made validation
        if len(data['date_made']) < 3:
            flash("Date must be selected",'error_recipe')
            is_valid = False
        
        # under 30 validation
        if not 'under_thirty' in data:
            flash("Yes/No needs to be chosen",'error_recipe')
            is_valid = False
            
        return is_valid