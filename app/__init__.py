from flask import Flask

# Initialize the Flask app
app = Flask(__name__, template_folder='../templates', static_folder='../static')

from app import routes
