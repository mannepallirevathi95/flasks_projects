from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from shortenlinks import createid
import re

url_app = Flask(__name__)

url_app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite:///dn.sqlite3'
db = SQLAlchemy(url_app)

class LINKS(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    link = db.Column(db.String(1000))
    linkid = db.Column(db.String(6),unique = True)

def addnewlink(url):
    id = createid()
    if str(LINKS.query.filter_by(linkid = id).first()) != "None":
        while  str(LINKS.query.filter_by(linkid = id).first()) != "None":
            id = createid()
    newlink = LINKS(link = url, linkid = id)
    db.session.add(newlink)
    db.session.commit()
    return id

@url_app.route('/')
def home():
    return render_template('home.html', message = 'SHORTEN YOUR URL')

@url_app.route('/shorten', methods = ['POST'])
def shorten():
    link = request.form['link']
    if re.search('https?://\w+.\w+.+' ,link) == None:
        return render_template('home.html', message = 'NOT A VALID')
    linkid = addnewlink(link)
    return render_template('home.html', message = linkid)

@url_app.route('/<linkid>')
def redir(linkid):
    link = LINKS.query.filter_by(linkid = linkid).first()
    return redirect(link.link)


if __name__ == "__main__" :
    db.create_all()
    url_app.run(debug=True)