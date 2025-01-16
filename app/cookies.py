import json
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

@app.route('/set-cookies', methods=['POST'])
def set_cookies():
    data = request.json

    username = data.get('username')
    owned_sets = data.get('ownedSets', [])
    wishlist_sets = data.get('wishlistSets', [])

    if not username:
        return jsonify({'error': 'Username is required'}), 400
    # Create response and set cookies
    response = make_response(jsonify({'message': 'Cookies set successfully'}))
    response.set_cookie('username', username, httponly=True, samesite='Strict', secure=True, max_age=3600)
    response.set_cookie('ownedSets', json.dumps(owned_sets), httponly=True, samesite='Strict', secure=True, max_age=3600)
    response.set_cookie('wishlist', json.dumps(wishlist_sets), httponly=True, samesite='Strict', secure=True, max_age=3600)

    return response


