from flask import Flask, session
from flask_session import Session
from flask_bootstrap import Bootstrap
from flask_cors import CORS
import os

UPLOAD_FOLDER = './app/static/upload/'

app = Flask(__name__)
# Check Configuration section for more details
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

from app import routes

bootstrap = Bootstrap(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['SECRET_KEY'] =  os.urandom(12).hex()