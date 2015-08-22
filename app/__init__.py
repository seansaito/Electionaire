from flask import Flask
app = Flask(__name__)

# Last line to avoid import errors
from app import views
