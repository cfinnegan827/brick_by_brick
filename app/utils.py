import requests
from app.config.brickset_config import BRICKSET_API_KEY, BRICKSET_USERNAME, BRICKSET_PASSWORD
from app.config.firebaseConfig import db
import json
import bcrypt

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


def get_set_by_params(params):
    url = f"{API_URL}/getSets"
    user_hash = authenticate()
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
            # for set_info in data["sets"]:
            #     print(f"Name: {set_info['name']}")
            #     print(f"Theme: {set_info['theme']}")
            #     print(f"Set ID: {set_info['setID']}")
            #     print(f"Year: {set_info['year']}")
            #     print(f"Pieces: {set_info.get('pieces', 'N/A')}")
            #     print(f"Set Image: {set_info['image'], 'N/A'}\n")
            return data["sets"]
        else:
            print("No sets found.")
    else:
        print(f"Error: {response.status_code}")


#adds a user to the firebase database
def add_user_to_db(username,password,email,fullName):
    """
    Adds a user to Firestore with the username as the document ID.
    """
    try:
        username = username
        hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db.collection("users").document(username).set({
            "username": username,
            "password": hash_password.decode('utf-8'),
            "name": fullName,
            "email": email,
            "ownedSets": [],
            "wishlistSets": []
        })
        return True
    except Exception as e:
        raise Exception(f"Error adding user to Firestore: {str(e)}")
    
#authenticates a user by username and password
def authenticate_user_in_db(username, password):
    """
    takes a users username and password and authenticates them, if authentication
    passes user can log in succesfully
    """
    username = username
    password = password.encode('utf-8')
    try:
        userRef = db.collection('users').document(username)
        user = userRef.get()

        if not user.exists:
            raise ValueError(f"User {username} not found")
        
        stored_password = user.to_dict()['password'].encode('utf-8')

        if bcrypt.checkpw(password, stored_password):
            return True
    except Exception as e:
        return f"Error verifying password: {str(e)}"
    
#given a username gets both set list of  a user for cookies
def get_users_set_lists(username):
    userRef = db.collection('users').document(username)
    user = userRef.get().to_dict()
    ownedSets = user['ownedSets']
    wishlist = user['wishlistSets']
    return ownedSets, wishlist

# trims the set list down to only necessary components
def trim_sets():
    trimmed_sets = []
    return trimmed_sets

# takes a dictionary of sets and cuts it into pages of 12, 3 across 4 down
def make_pages(all_sets):
    set_pages = {}
    page_length = 12
    while len(all_sets > 0):
        return
    return