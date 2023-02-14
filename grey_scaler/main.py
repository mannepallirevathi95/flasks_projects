from email import message
from flask import Flask, render_template,redirect,request,send_file,url_for
from werkzeug.utils import secure_filename
import os
from processor import processor
from flask_apscheduler import APScheduler

scheduler = APScheduler()

g_app = Flask(__name__)

UPLOAD_FOLDER = './static/process/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
g_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
g_app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

@g_app.route('/')
def home():
    return render_template("home.html", message = 'GREY SCALER')

@g_app.route('/process/', methods = ['POST', 'GET'])
def process():
    f = request.files['file']

    if f.filename == '':
        return render_template('home.html', message='PLEASE SELECT')
    
    if f.filename.split('.')[1] in g_app.config['ALLOWED_EXTENSIONS']:
        f.save(os.path.join(g_app.config['UPLOAD_FOLDER'], f.filename))
        processor(f.filename)
        return redirect(url_for('download', filename = f.filename))

    else:
        return render_template('home.html', message='NOT VALID')

@g_app.route('/download/<filename>')
def download(filename):
    filelocation = './static/process/' + filename
    return send_file(filelocation, as_attachment=True)

def emptyfolder():
    filelist=[f for f in os.listdir('./static/process/')]
    for f in filelist: 
      os.remove(os.path.join('./static/process/',f))
      
if __name__ == "__main__":
    scheduler.add_job(id='empty folder', func=emptyfolder, trigger='interval', seconds=4)
    scheduler.start()
    g_app.run(debug = True)