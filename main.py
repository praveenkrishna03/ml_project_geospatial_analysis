import collections
from flask import *
from flask import request, flash
from flask import Flask, request, render_template, redirect, url_for
from modules import ml_module
import json
import os
from flask_login import LoginManager, login_user, UserMixin
from pymongo import MongoClient
import bcrypt

main_user = ''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dbda562a07158c2cd81f6de86f656522'
JSON_FILE = 'data.json'

def load_json_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []

def save_json_data(data):
    with open(JSON_FILE, 'w') as f:
        json.dump(data, f)

def trim_json_file(filename):
    try:
        with open(filename, 'r+') as file:
            data = json.load(file)
            if len(data) > 3:
                trimmed_data = data[-3:]
                file.seek(0) 
                json.dump(trimmed_data, file, indent=4)
                file.truncate() 
                print(f"File '{filename}' successfully trimmed.")
            else:
                print(f"File '{filename}' contains 3 or fewer items. No trimming needed.")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file '{filename}'.")
    

@app.route('/', methods=['GET'])
def first_page():
    return render_template('firstpage.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        trim_json_file('data.json')
        response_data = load_json_data()
        user1 = [{'name' : main_user}]
        print(user1)
        print('hello')
        return render_template("index.html", response_data=response_data, user=user1)
    else:
        topic = request.json.get('topic')
        result = ml_module.get_label(topic)
        data = load_json_data()
        data.append(result)
        save_json_data(data)
        return redirect(url_for('home', username=main_user))

@app.route('/current_fallow',methods=['GET'])
def current_fallow():
    return render_template("map_current_fallow.html")

@app.route('/deciduous_woodlands',methods=['GET'])
def deciduous_woodlands():
    return render_template("map_deciduous_woodlands.html")

@app.route('/littoral_swamp',methods=['GET'])
def littoral_swamp():
    return render_template("map_littoral_swamp.html")

@app.route('/snowfall',methods=['GET'])
def snowfall():
    return render_template("map_snowfall.html")

@app.route('/plantation',methods=['GET'])
def plantation():
    return render_template("map_plantation.html")

@app.route('/waterbodies',methods=['GET'])
def waterbodies():
    return render_template("map_waterbodies.html")

@app.route('/get-maps', methods=['GET'])
def get_maps():
    return render_template('map_data.html')

@app.route('/about_us',methods=['GET'])
def about_us():
    return render_template('about_us.html')


def MongoDB():
    #uri = f"mongodb+srv://{ashwant41}:{password}@zerocluster.ile1ck5.mongodb.net/?retryWrites=true&w=majority"
    #client = MongoClient(uri)
    client = MongoClient("mongodb+srv://ashwant41:ip-project@zerocluster.ile1ck5.mongodb.net/?retryWrites=true&w=majority&appName=ZeroCluster")
    db = client['user']  
    collection = db['user_det'] 
    return collection


login_manager = LoginManager()
login_manager.init_app(app)

# User model
class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.password = password

# Sample users (replace with your actual user data)
users = {'username': User('username', 'password')}

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/login_or_signup', methods=['GET', 'POST'])
def login_or_signup():
    if request.method == 'POST':
        if request.form['action'] == 'login':
            # Handle login
            username = request.form['username']
            password = request.form['password']
            if check_credentials(username, password):
                # Log the user in
                    username_found = MongoDB().find_one({"username": username})
                    username_val = username_found['username']
                    passwordcheck = username_found['password']
                    main_user = username_val
                    print(main_user)
                    print('hello')
                    #encode the password and check if it matches
                    if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                        session["username"] = username_val
                        return redirect(url_for('home',username=main_user))
                    else:
                        if "username" in session:
                            return redirect(url_for("login_or_signup"))
                        message = 'Wrong password'
                    return redirect(url_for('home'))
            else:
                flash('Invalid username or password', 'error')
                return render_template('login.html')

        elif request.form['action'] == 'signup':
            # Handle signup
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['con_password']
            if password == confirm_password:
                if create_user(username, password):
                    flash('Account created successfully', 'success')
                    return redirect(url_for('home'))  # Redirect to login after signup
                else:
                    flash('Failed to create account', 'error')
                    return redirect(url_for('login_or_signup'))
            else:
                flash('Passwords do not match', 'error')
                return redirect(url_for('login_or_signup'))
    else:
        return render_template('login.html')
    
def check_credentials(username, password):
    username_found = MongoDB().find_one({"username": username})
    return username_found

def create_user(username, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        existing_user = MongoDB().find_one({'username': username})
        if existing_user:
            flash('User already exists', 'error')
            return redirect(url_for('login_or_signup'))
        MongoDB().insert_one({'username': username, 'password': hashed_password})
        flash('Account created successfully', 'success')
        return False
if __name__ == '__main__':
    app.run(debug=True)
