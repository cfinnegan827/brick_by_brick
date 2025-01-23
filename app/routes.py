from flask import request, jsonify, render_template, redirect, url_for, session
from .utils import *
from datetime import timedelta
import json
from app import app


app.secret_key = 'your_secret_key_here'
app.permanent_session_lifetime = timedelta(hours=5)


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/profile-page')
def profile_page():
    if 'username' in session:
        username = session['username']
        return render_template('profile.html', username = username)
    return redirect(url_for('index'))

@app.route('/settings')
def settings_page():
    if 'username' in session:
        username = session['username']
        return render_template('settings.html', username = username)
    return redirect(url_for('index'))

@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        return render_template('home.html', username = username)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
    # Clear the session when logging out
    session.pop('username', None)
    session.pop('ownedSets', None)
    session.pop('wishlistSets', None)
    return redirect(url_for('index'))  # Redirect to login page

@app.route('/authenticate-user', methods=['POST'])
def authenticate_user():
    username = request.form['username']
    password = request.form['password']
    try:
        if authenticate_user_in_db(username, password):
            ownedSets, wishlistSets = get_users_set_lists(username)
            session.permanent = True
            session['username'] = username
            session['ownedSets'] = ownedSets
            session['wishlistSets'] = wishlistSets
            return redirect(url_for('home')) #fix this to add cookies using session nect time.
        return redirect(url_for('index'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
@app.route('/get-sets', methods=['POST'])
def get_sets():
    input_data = request.json
    if not input_data:
        return jsonify({"error": "Invalid input, expected JSON"}), 400
    user_hash = authenticate()
    if not user_hash:
        return jsonify({"error": "invalid user hash data authentication failed"}), 401
    try:
        params = input_data.get('params', {})
        sets = get_set_by_params(user_hash, params)
        return jsonify({"success": True, "sets": sets})
    except Exception as e:
        return jsonify({"error": str(e)}), 500