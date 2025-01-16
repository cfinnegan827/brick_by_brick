from firebase_admin import credentials, initialize_app, firestore

cred = credentials.Certificate("brick_by_brick_service_key.json")
initialize_app(cred)

db = firestore.client()
