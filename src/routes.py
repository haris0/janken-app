import os
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from src import src
from keras.preprocessing import image
import numpy as np
from keras.models import load_model


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@src.route('/')
@src.route('/index')
def index():
    user = {'username': 'Riza'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home')

def img_predict(path):
    model_stock = load_model('./src/model_rps.h5')
    
    img = image.load_img(path, target_size=(200,200))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    classes = model_stock.predict(images, batch_size=10)

    return classes

@src.route('/', methods=['GET', 'POST'])
@src.route('/index', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(src.config['UPLOAD_FOLDER'], filename)
            file.save(path)            
            classes = img_predict(path)
            print(classes)
            return render_template('index.html', title='Home')

@src.route('/about')
def about():
    return render_template('about.html', title='About')

@src.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404