import requests
from app.config import BRICKSET_API_KEY, BRICKSET_USERNAME, BRICKSET_PASSWORD
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