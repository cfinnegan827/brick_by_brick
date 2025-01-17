from flask import request, jsonify, render_template
import utils as util
import json
from app import app




@app.route('/')
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
        data = request.json
        if not data:
            return jsonify({"error": "not data provided"}), 400
        message = util.add_user_to_db(data)
        return jsonify({"message": message}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#get all sets based on a set of params using get_set_by_params function
@app.route('/get-sets', methods=['POST'])
def get_sets():
    input_data = request.json
    if not input_data:
        return jsonify({"error": "Invalid input, expected JSON"}), 400
    user_hash = util.authenticate()
    if not user_hash:
        return jsonify({"error": "invalid user hash data authentication failed"}), 401
    try:
        params = input_data.get('params', {})
        sets = util.get_set_by_params(user_hash, params)
        return jsonify({"success": True, "sets": sets})
    except Exception as e:
        return jsonify({"error": str(e)}), 500