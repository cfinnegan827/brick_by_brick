import requests
from app.config.brickset_config import BRICKSET_API_KEY, BRICKSET_USERNAME, BRICKSET_PASSWORD
from app.config.firebaseConfig import db
import json

API_URL = "https://brickset.com/api/v3.asmx"

# authenticate the user using login and gets userhash to use in later api calls
def authenticate():
    url = f"{API_URL}/login"
    params = {
        "apiKey": BRICKSET_API_KEY,
        "username": BRICKSET_USERNAME,
        "password": BRICKSET_PASSWORD
    }
    response = requests.get(url, params)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            print("Successfully authenticated!")
            return data["hash"]
        else:
            print("Authentication failed:", data["message"])
    else:
        print(f"Error: {response.status_code}")
    return None


def get_set_by_params(user_hash, params):
    url = f"{API_URL}/getSets"
    params = {
        "apiKey": BRICKSET_API_KEY,
        "userHash": user_hash,
        "params": json.dumps(params)
    }
    print("made it here")
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "sets" in data:
            for set_info in data["sets"]:
                print(f"Name: {set_info['name']}")
                print(f"Theme: {set_info['theme']}")
                print(f"Set ID: {set_info['setID']}")
                print(f"Year: {set_info['year']}")
                print(f"Pieces: {set_info.get('pieces', 'N/A')}")
                print(f"Set Image: {set_info['image']['imageURL']}\n")
            return data["sets"]
        else:
            print("No sets found.")
    else:
        print(f"Error: {response.status_code}")


#adds a user to the firebase database
def add_user_to_db(data):
    """
    Adds a user to Firestore with the username as the document ID.
    """
    try:
        if "username" not in data or not data["username"]:
            raise ValueError("Username is required to add user")
        
        username = data['username']
        db.collection("users").document(username).set({
            "username": username,
            "name": data["fullName"],
            "email": data["email"],
            "ownedSets": [],
            "wishlistSets": []
        })
        return f"User created succesfully: {username}"
    except Exception as e:
        raise Exception(f"Error adding user to Firestore: {str(e)}")
