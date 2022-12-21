from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import jwt
from time import time

db = SQLAlchemy()

# This defines the user database for sqlalchemy
# and allows us to make changes which sqlalchmey.
# Also defines a method for creating a jwt token for
# password reset and verifys that token for password reset.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    def get_user_reset_token(self, expires_in=600):
        return jwt.encode(
            {'reset-password': self.id, 'exp': time() + expires_in}, '\xdb\x11D\x04\xa8\x84*\x82\x0fm8\xf9\x8e\x9aGE\xa6\xf0r\xe4\x90\xe9\xb9o<gd\x9d\xcb\xef', algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, '\xdb\x11D\x04\xa8\x84*\x82\x0fm8\xf9\x8e\x9aGE\xa6\xf0r\xe4\x90\xe9\xb9o<gd\x9d\xcb\xef',
                            algorithms=['HS256'])['reset-password']
        except:
            return
        return User.query.get(id)

# Define a object for the files database for the users files
# work in progress
class User_Files(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    file_name = db.Column(db.String(30), nullable=False, unique=True)
    file_blob = db.Column(db.String(1000), nullable=False)

# converts files to a blob format for db storage
def convertToBlob(file_path):
    with open(file_path, 'rb') as file:
        binary = file.read()
    return binary

# Adds the users to the database
def addusertodb(email, password):
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()

# Changes the users password
def commitnewpassword(email, new_password):
    user = User.query.filter_by(email=email).first()
    print(user.password)
    user.password = new_password
    print(user.password)
    db.session.add(user)
    db.session.commit()