from firebase_admin import credentials, initialize_app, firestore

cred = credentials.Certificate("app/config/service_key.json")
initialize_app(cred)

db = firestore.client()
