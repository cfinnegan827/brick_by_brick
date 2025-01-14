from flask import Flask, request, jsonify
from utils import get_set_by_params, authenticate
import json


app = Flask(__name__)


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