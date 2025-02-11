import requests
from app.config.brickset_config import BRICKSET_API_KEY, BRICKSET_USERNAME, BRICKSET_PASSWORD
from app.config.firebaseConfig import db
import json
import bcrypt
from firebase_admin import firestore
import ast

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
            sets = trim_sets(data['sets'])
            return sets
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
    password = password.encode('utf-8')
    try:
        userRef = db.collection('users').document(username)
        user = userRef.get()
        if not user.exists:
            return False
        
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
def trim_sets(all_sets):
    trimmed_sets = []
    for set in all_sets:
        #trim down the set to name, id, price, image, etc.
        new_set = {
            'setID': set.get('setID'),
            'number': set.get('number'),
            'name': set.get('name'),
            'year': set.get('year'),
            'theme': set.get('theme'),
            'subtheme': set.get('subtheme'),
            'pieces': set.get('pieces'),
            'price' : set.get('LEGOCom').get('US').get('retailPrice'),
            'image': set.get('image').get('imageURL') if set.get('image').get('imageURL') else ''
        }
        trimmed_sets.append(new_set)
    return trimmed_sets

#add sets to wishlist or the owned sets
def add_set_to_wishlist(username, set_to_add):
    db.collection("users").document(username).update({
        'wishlistSets': firestore.ArrayUnion([set_to_add])
        })
    return 'added set to wishlist'

def add_set_to_ownedlist(username, set_to_add):
    db.collection("users").document(username).update({
    'ownedSets': firestore.ArrayUnion([set_to_add])
    })
    return 'added set to wishlist'



#checks to see if a user has a set in either of their set list
def check_dup_owned(username, set_to_check):
    temp_sets = db.collection('users').document(username).get().to_dict()
    if temp_sets:
        sets = temp_sets.get('ownedSets')
        for set in sets:
            if set == set_to_check:
                return False
    return True

def check_dup_wishlist(username, set_to_check):
    temp_sets = db.collection('users').document(username).get().to_dict()
    if temp_sets:
        sets = temp_sets.get('wishlistSets')
        for set in sets:
            if set == set_to_check:
                return False
    return True

def get_wishlist_sets_db(username):
    sets = db.collection('users').document(username).get().to_dict()
    if not sets:
        return
    return sets.get('wishlistSets')

def get_owned_sets_db(username):
    sets = db.collection('users').document(username).get().to_dict()
    if not sets:
        return
    return sets.get('ownedSets')

#gets most recent set added and returns the image
def get_recent_owned_image(username):
    owned_Sets = get_owned_sets_db(username)
    if owned_Sets:
        data_dicts = [ast.literal_eval(item) for item in owned_Sets]
        recent_Set_image = data_dicts[len(owned_Sets)-1].get('image')
        return recent_Set_image
    return

def get_recent_wishlist_image(username):
    wishlist_sets = get_wishlist_sets_db(username)
    if wishlist_sets:
        data_dicts = [ast.literal_eval(item) for item in wishlist_sets]
        recent_Set_image = data_dicts[len(wishlist_sets)-1].get('image')
        return recent_Set_image
    return
