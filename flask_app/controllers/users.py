from flask import render_template, redirect, request, flash, session
from flask_app.models.user import User
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def home():
    if User.validate_session():
        return redirect("/dashboard")
    else:
        return render_template('index.html')

# @app.route('/dashboard')
# def display_dashboard():
#     if not User.validate_session():
#         return redirect("/")
#     else:
#         data = {
#             'id': session['id']
#         }

#         return render_template("dashboard.html", current_user = User.get_recipes(data))


@app.route('/register', methods = ['POST'])
def create_user():
    if not User.validate_registration(request.form):
        return redirect('/')
    
    else:
        if User.get_one({'email':request.form['email']}) == None:
            data = {
                'first_name': request.form['first_name'],
                'last_name':request.form['last_name'],
                'email':request.form['email'],
                'password':bcrypt.generate_password_hash(request.form['password'])
            }
            user_id= User.save(data)
            session['first_name'] = request.form['first_name']
            session['last_name'] = request.form['last_name']
            session['emaiil'] = request.form['email']
            session['id'] = user_id
            return redirect('/dashboard')
        else:
            flash("This email has already been registered! Please use a different one.", "error_reg")
            return redirect('/')
            
        
@app.route('/login', methods = ['POST'])
def login():
    if not User.validate_login(request.form):
        flash("Invalid credentials!","error_login")
        return redirect('/')
    else:
        result = User.get_one( request.form )

        if result == None:
            flash("Wrong credentials" , "error_login")
            return redirect('/')
        else:
            if not bcrypt.check_password_hash ( result.password, request.form['password']):
                flash("Wrong credentials, try again", "error_login")
                return redirect("/")
            else:
                session['first_name'] = result.first_name
                session['last_name'] = result.last_name
                session['emaiil'] = result.email
                session['id'] = result.id
                return redirect('/dashboard')    
            
@app.route('/logout', methods = ['POST'] )
def logout():
    session.clear()
    return redirect('/')