from flask import Flask
from flask_bootstrap import Bootstrap

UPLOAD_FOLDER = './src/static/upload/'

src = Flask(__name__)

from src import routes

bootstrap = Bootstrap(src)
src.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER