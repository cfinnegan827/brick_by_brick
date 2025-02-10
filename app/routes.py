from flask import request, jsonify, render_template, redirect, url_for, session
from .utils import *
from datetime import timedelta
import json
from app import app


app.secret_key = 'brick_by_brick_secret_key'
app.permanent_session_lifetime = timedelta(hours=1)

#initial app route that redirectsd a user to the login screen if they arent signed in 
# or the home screen if you are logged in
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

# app route for the profile pagewhere a user can adjust their sets list and their settings
@app.route('/profile-page')
def profile_page():
    if 'username' in session:
        username = session['username']
        owned_set_image = get_recent_owned_image(username)
        wishlist_set_image = get_recent_wishlist_image(username)
        return render_template('profile.html', username = username, recent_owned_image = owned_set_image, recent_wishlist_image = wishlist_set_image)
    return redirect(url_for('index'))

# app route for the settings page for the user
@app.route('/settings')
def settings_page():
    if 'username' in session:
        username = session['username']
        return render_template('settings.html', username = username)
    return redirect(url_for('index'))

# app.route for the home page of the user where they can pick a direction to interact
@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        return render_template('home.html', username = username)
    return redirect(url_for('index'))

# simple app route to render the login page
@app.route('/login')
def login():
    return render_template('login.html')

#simple app route to render the registration page
@app.route('/register')
def register():
    return render_template('register.html')

#app route for the owned sets page that is accessed in prfile page
@app.route('/owned-sets')
def owned_sets():
    if 'username' in session:
        username = session['username']
        owned_sets = get_owned_sets_db(username)
        return render_template('/sets/ownedSets.html', sets = owned_sets)
    return redirect(url_for('index'))

#app route for the owned sets page that is accessed in prfile page
@app.route('/wishlist-sets')
def wishlist_sets():
    if 'username' in session:
        username = session['username']
        owned_sets = get_wishlist_sets_db(username)
        return render_template('/sets/wishlistSets.html', sets = owned_sets)
    return redirect(url_for('index'))

# app route for the add sets page where users add sets to a specific list(owned or wishlist) if they want
@app.route('/add-sets')
def add_sets():
    return render_template('/sets/addSets.html')

# app route for a user to logout, where all cookies are popped out of the session and the user
# is redirected to the login page
@app.route('/logout')
def logout():
    # Clear the session when logging out
    session.pop('username', None)
    return redirect(url_for('index'))  # Redirect to login page

# authenticates a user by taking info from the login form submission and 
# checks to see if the users entered password matches for the username they entered
@app.route('/authenticate-user', methods=['POST'])
def authenticate_user():
    username = request.form['username']
    password = request.form['password']
    try:
        if authenticate_user_in_db(username, password):
            session.permanent = True
            session['username'] = username
            return redirect(url_for('home')) #fix this to add cookies using session nect time.
        return redirect(url_for('index'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# add a user to the db by calling the util function for adding user and takes the 
# submission from the form
@app.route('/add-user', methods=['POST'])
def add_user():
    try:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        fullName = request.form['fullName']
        if add_user_to_db(username,password,email,fullName):
            return redirect(url_for('login'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#get all sets based on a set of params using get_set_by_params function
@app.route('/get-sets', methods=['GET'])
def get_sets():
    theme = request.args.get('theme', default=None, type=str)
    year = request.args.get('year', default=None, type=str)
    query = request.args.get('query', default=None, type=str)
    param = ['theme', 'year', 'query']
    args = [theme, year, query]
    params = {}
    # Only include non-empty parameters in the search
    for i in range(0,3):
        if args[i]:
            params[param[i]] = args[i]
    sets = get_set_by_params(params)
    if sets:
        return render_template('/sets/addSets.html', sets=sets)
    sets_error = "no sets found"
    return render_template('/sets/addSets.html', error=sets_error)



@app.route('/add-wishlist', methods=['POST'])
def add_to_wishlist():
    username = session['username']
    set_to_add = request.form['set_to_add']
    if check_dup_wishlist(username, set_to_add):
        add_set_to_wishlist(username, set_to_add)
        return redirect(url_for('add_sets')) # Tell frontend to reload
    else:
        sets_error = f"{set_to_add} is a already in your wishlist set list"
        return render_template('/sets/addSets.html', error=sets_error)

@app.route('/add-owned', methods=['POST'])
def add_to_owned():
    set_to_add = request.form['set_to_add'] 
    username = session['username']
    if check_dup_owned(username, set_to_add):
        add_set_to_ownedlist(username, set_to_add)
        return redirect(url_for('add_sets')) # Tell frontend to reload
    else:
        sets_error = f"{set_to_add} is a already in your owned set list"
        return render_template('/sets/addSets.html', error=sets_error)
    
