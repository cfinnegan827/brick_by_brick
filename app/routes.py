from flask import request, jsonify, render_template, redirect, url_for
from .utils import *
import json
from app import app




@app.route('/home')
def index():
    return render_template('index.html')
    
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/add-user', methods=['POST'])
def add_user():
    try:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        fullName = request.form['fullName']
        add_user_to_db(username,password,email,fullName)
        return redirect(url_for('index'))
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