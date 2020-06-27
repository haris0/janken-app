from app import app
import os
from flask import Flask, render_template, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import numpy as np
from module.janken import img_predict, janken_game


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    pointx, pointy = 0, 0
    session['pointx'] = 0, 
    session['pointy'] = 0,
    return render_template('index.html', title='Home', pointx=pointx, pointy=pointy)

def cleaning_upload_dic(path):
    if not os.listdir(path):
        print('Folder Empty')
    else:
        filelist = [ f for f in os.listdir(path)]
        for f in filelist:
            os.remove(os.path.join(path, f))

@app.route('/index', methods=['GET', 'POST'])
def upload_file():

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

            pointx = session['pointx'][0]
            pointy = session['pointy'][0]

            if game_result != "Draw":
                if game_result == "Win":
                    pointx += 1
                else:
                    pointy += 1
            
            session['pointx'] = pointx, 
            session['pointy'] = pointy,
            
            result = {
                'user':user,
                'comp':comp,
                'result':game_result,
                'file':filename
            }

            return render_template('index.html', title='Home', result=result, pointx=pointx, pointy=pointy)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404