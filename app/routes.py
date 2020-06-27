import os
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from app import app
import numpy as np
from module.janken import img_predict, janken_game


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

point = {
    'user': 0,
    'comp': 0
}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    global point
    point['user'] = 0
    point['comp'] = 0
    return render_template('index.html', title='Home', point=point )

def cleaning_upload_dic(path):
    if not os.listdir(path):
        print('Folder Empty')
    else:
        filelist = [ f for f in os.listdir(path)]
        for f in filelist:
            os.remove(os.path.join(path, f))

@app.route('/index', methods=['GET', 'POST'])
def upload_file():
    global point    
    cleaning_upload_dic(app.config['UPLOAD_FOLDER'])
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
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)            
            classes = img_predict(path)
            
            user, comp, game_result = janken_game(classes)
            
            if game_result != "Draw":
                if game_result == "Win":
                    point['user'] += 1
                    point['comp'] = point['comp']
                elif game_result == "Lose":
                    point['comp'] += 1
                    point['user'] = point['user']
            else:
                point['user'] = point['user']
                point['comp'] = point['comp']

            result = {
                'user':user,
                'comp':comp,
                'result':game_result,
                'file':filename
            }
            return render_template('index.html', title='Home', result=result, point=point)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404