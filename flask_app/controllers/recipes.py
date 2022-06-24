import re
from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models import user
from flask_app.models.recipe import Recipe

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@app.route('/recipes')
@app.route('/dashboard')
def display_recipes():
    if not user.User.validate_session():
        return redirect("/")
    else:
        recipes = Recipe.get_all()
        return render_template("dashboard.html",recipes = recipes)
    
@app.route('/recipes/new')
def display_form():
    if not user.User.validate_session():
        return redirect("/login")
    else:      
        return render_template("createRecipe.html")


@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if not user.User.validate_session():
        return redirect("/login")
    else:
        if not Recipe.validate_form(request.form):
            return redirect('/recipes/new')  
        else:    
            data = {
                'name' : request.form['name'],
                'description' : request.form['description'],
                'instructions' : request.form['instructions'],
                'date_made' : request.form['date_made'],
                'under_thirty' : request.form['under_thirty'],
                'user_id' : session['id']
            }
            Recipe.save(data)
            return redirect("/dashboard")

@app.route('/recipes/<int:id>')
def show_one_recipe(id):
    if not user.User.validate_session():
        return redirect("/login")
    else:      
        data = {
            "id":id
        }
        current_recipe = Recipe.get_one(data)
        return render_template("showRecipe.html", current_recipe=current_recipe )

@app.route('/recipes/delete/<int:id>')
def delete(id):
    if not user.User.validate_session():
        return redirect("/login")
    else:      
        data = {
            "id":id
        }
        Recipe.delete_one(data)
        return redirect("/dashboard",)


@app.route('/recipes/edit/<int:id>')
def display_edit(id):    
    if not user.User.validate_session():
        return redirect("/login")
    else:      
        data = {
            "id":id
        }
        
        current_recipe = Recipe.get_one(data)
        
        return render_template("editRecipe.html", current_recipe=current_recipe )

@app.route('/recipes/edit/<int:id>', methods = ['POST'])
def update_recipe(id):   
    if not user.User.validate_session():
        return redirect("/login")
    else:    
        if not Recipe.validate_form(request.form):
            data = {
                'id':id
            }
            # redirect to edit recipe page
            return redirect(f'/recipes/edit/{id}')  
        else:        
            data = {
                'id' : id,
                'name' : request.form['name'],
                'description' : request.form['description'],
                'instructions' : request.form['instructions'],
                'date_made' : request.form['date_made'],
                'under_thirty' : request.form['under_thirty'],
                'user_id' : session['id']
            }
            
            Recipe.update_one(data)
            return redirect('/dashboard')


