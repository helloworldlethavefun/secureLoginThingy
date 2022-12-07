# import needed modules
from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User
from flask_login import LoginManager

# initilize flask, login manager and sqlalchmey
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'thisisakeyfornowwillchangelater'
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# just the index route
@app.route('/')
def index():
    return render_template('index.html')

# if posted to request to view the posted info then store in a variable
@app.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        return render_template('index.html')
    else:
        return render_template('register.html')

# as long as it's not imported as a module
# run the applicatoin on port 5000 and enable debug
if __name__ == "__main__":
    app.run(port=8000, debug=True)