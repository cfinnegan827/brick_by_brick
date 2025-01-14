import requests
from app.config import BRICKSET_API_KEY, BRICKSET_USERNAME, BRICKSET_PASSWORD
import json

API_URL = "https://brickset.com/api/v3.asmx"

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
            return data['sets']
        else:
            print(data)
            print("No sets found.")
    else:
        print(f"Error: {response.status_code}")

def get_sets( page_size, page_number, query, user_hash):
    url = f"{API_URL}/getSets"
    params = {
        "apiKey": BRICKSET_API_KEY,
        "userHash": user_hash,
        "params": json.dumps({
            "query": query,
            "pageSize": page_size,
            "pageNumber": page_number
        })

    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        try:
            data = response.json()
            if "sets" in data:
                print(f"Displaying page {page_number} (showing {page_size} sets per page):")
                for lego_set in data["sets"]:
                    print(f"Name: {lego_set['name']}")
                    print(f"Set Number: {lego_set['setID']}")
                    print(f"Year: {lego_set['year']}")
                    print(f"Pieces: {lego_set.get('pieces', 'N/A')}")
                    print(f"Minifigs: {lego_set.get('minifigs', 'N/A')}")
                    print(f"Set Image: {lego_set['image']['imageURL']}\n")
            else:
                print("No sets found.")
        except ValueError:
            print("Error: Unable to parse JSON response.")
    else:
        print(f"Error: {response.status_code}")


def get_themes():
    url = f"{API_URL}/getThemes"
    params = {"apiKey": BRICKSET_API_KEY}
    response = requests.get(url, params)
    data = response.json()
    themes = data.get("themes", [])
    for theme in themes:
        print(f"Theme: {theme['theme']}")
        print(f"Set Count: {theme['setCount']}")
        print(f"Subtheme Count: {theme['subthemeCount']}")
        print(f"Year From: {theme['yearFrom']}")
        print(f"Year To: {theme['yearTo']}\n")
    return themes

def set_images(user_hash, params):
    sets = get_set_by_params(user_hash, params)
    for set in sets:
        set_image = set['image']['imageURL']
    return set_image
# Fetch the first page of 15 sets
params = {'theme':'botanicals'}  # Death Star

# Get historical price from bricklink
user_hash = authenticate()
get_set_by_params(user_hash, params)
