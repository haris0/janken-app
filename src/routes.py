import os
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from src import src
import numpy as np
from module.janken import img_predict

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@src.route('/')
def root():
    return redirect(url_for('index'))

@src.route('/index')
def index():
    return render_template('index.html', title='Home')

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
    return render_template('404.html'), 404