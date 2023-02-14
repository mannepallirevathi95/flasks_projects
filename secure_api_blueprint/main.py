from flask import Flask, jsonify, request , make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
import uuid
import jwt 
import datetime
from functools import wraps
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///mydb.db'
db= SQLAlchemy(app)
app.config['SECRET_KEY']='MYSUPERSECRET'



class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    public_id=db.Column(db.String(50),unique=True)
    username=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(50),nullable=False)
    admin=db.Column(db.Boolean,default=False)

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=None
        if 'x-access-token' in request.headers:
            token= request.headers['x-access-token']
        if not token:
            return jsonify({'message':'Token is missing'}),401 
        try:
            data= jwt.decode(token,app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user,*args,**kwargs)
    return decorated


@app.route('/data')
@token_required
def getdata(current_user):
    print(current_user.username)
    return jsonify({'data':'topsecuredata'})


@app.route('/api/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    user=User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password,auth.password):
        token = jwt.encode({'public_id':user.public_id,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
        return jsonify({'token':token.decode('UTF-8')})


    return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login required!"'})


def createuser():
    password='boss'
    hashedpassword=generate_password_hash(password,method='sha256')
    new_user=User(
        public_id=str(uuid.uuid4()),
        username='boss',
        password=hashedpassword)
    db.session.add(new_user)
    db.session.commit()
#createuser()

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
