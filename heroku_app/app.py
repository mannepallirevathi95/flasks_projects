from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
hk_app = Flask(__name__)

hk_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sridevi123@localhost/heroku_DB'
db = SQLAlchemy(hk_app)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_

@hk_app.route('/')
def index():
    return render_template("index.html")

@hk_app.route("/success", methods=['POST'])
def success():
        email = request.form["email_name"]
        height = request.form["height_name"]

        if db.session.query(Data).filter(Data.email_ == email).count() == 0:

            data = Data(email,height)
            db.session.add(data)
            db.session.commit()
            return render_template("success.html")

        return render_template('index.html',
        text = "user already exists, try new one")

if __name__ == "__main__":
    hk_app.run(debug = True)


