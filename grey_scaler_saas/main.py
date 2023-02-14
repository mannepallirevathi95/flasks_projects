from flask import Flask,render_template,flash,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.utils import secure_filename
import os
from processor import processor

login_app = Flask(__name__)
login_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy(login_app)
login_app.config['SECRET_KEY'] = 'SUPERSECRETKEY'

UPLOAD_FOLDER = './static/process/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
login_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

login_manager = LoginManager(login_app)

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(50),unique=True)
    password=db.Column(db.String(50),nullable=False)
    wallet= db.Column(db.Integer,default=0)
    hassubscription=db.Column(db.Boolean,default=0)
    

admin=Admin(login_app,name='ADMIN',template_mode='bootstrap3')
admin.add_view(ModelView(User,db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_app.route('/')
def home():
    return render_template('homepage.html')

@login_app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@login_app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('homepage.html')


@login_app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST' and request.form.get('username') and request.form.get('password'):
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username = username).first():
            user = User.query.filter_by(username = username).first()
            if user.password == password:
                login_user(user)
                flash('YOU ARE NOW LOGGED IN')
                return render_template('login.html')
            else:
                flash('WRONG PASSWORD')
                return render_template('login.html')
        else:
            flash('USER DO NOT EXISTS')
            return render_template('login.html')  

    flash('THIS IS A MESSAGE')
    return render_template("login.html")

def createuser(username, password):
    user = User(username = username, password = password)
    db.session.add(user)
    db.session.commit()
    


if __name__ == "__main__":
    db.create_all()
    login_app.run(debug=True)