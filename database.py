from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import jwt
from time import time

db = SQLAlchemy()

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

def addusertodb(email, password):
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()

def commitnewpassword(email, new_password):
    user = User.query.filter_by(email=email).first()
    print(user.password)
    user.password = new_password
    print(user.password)
    db.session.add(user)
    db.session.commit()