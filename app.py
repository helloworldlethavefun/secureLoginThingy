# import needed modules
from flask import Flask, render_template, redirect, url_for, request, session, abort, flash
from argon2 import PasswordHasher, Type
from argon2.exceptions import VerificationError
from database import db, User, addusertodb
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from form import LoginForm, RegisterForm, ResetPassword, ValidationError
import random
from emails import sendemail, mail
import pyotp

totc = pyotp.TOTP('base32secret3232', interval=600)
onetimecode = ''

def addnewpassword(email, new_password):
    user = User.query.filter_by(email=email).first()
    user.password = new_password
    print(user.password)


def sendotp(user_email):
    global onetimecode
    onetimecode = totc.now()
    sendemail(onetimecode, user_email)

ph = PasswordHasher(
    memory_cost=65536,
    time_cost=4,
    parallelism=2,
    hash_len=32,
    type=Type.ID,
    salt_len=16
)

class IncorrectPassword(Exception):
    pass


# initilize flask and register and error handler
# for status code 403
app = Flask(__name__)

@app.errorhandler(VerificationError)
def incorrectpassword(self):
    return '<script>alert("Incorrect Password"); window.location.replace("login");</script>'

@app.errorhandler(403)
def user_already_exist(self):
    return render_template('useralreadyexists.html'), 403

app.register_error_handler(403, user_already_exist)
app.register_error_handler(VerificationError, incorrectpassword)

# initilize the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'thisisakeyfornowwillchangelater'
db.init_app(app)

# setup the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# configure all of the mail stuffs
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "myflaskstuff@gmail.com"
app.config['MAIL_PASSWORD'] = 'zvoaekcscurfozsp'
mail.init_app(app)

@app.route('/create-new-password', methods=['POST', 'GET'])
def create_password():
    form = RegisterForm()
    return render_template('new-password.html', form=form)

@app.route('/password-reset/<token>', methods=['POST', 'GET'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    user = User.verify_reset_password_token(token)
    if not user:
        return 'not user'
    if user:
        form = RegisterForm()
        if form.validate_on_submit():
            email = user.email
            new_password = form.password.data
            hashed_password = ph.hash(new_password)
            addnewpassword(email, new_password)
        return render_template('new-password.html', form=form)

# page for entering the user email to send the one time reset code
@app.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user.email)
        sendemail(user)
        return redirect(url_for('login'))
    return render_template("reset-password-request.html", form=form)

# define the login manager for logging the user in and out
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# just the index route
@app.route('/')
def index():
    return render_template('index.html')

# basic dashboard page, will work on later
@app.route('/dashboard')
@login_required
def dashboard():
    print(current_user)
    return render_template('dashboard.html')

# logs the user out with the login manager
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# login page the takes the users email address and password hash
# then checks to verify the user input and db are the same then
# log the user in and direct to dashboard
@app.route('/login', methods=('POST', 'GET'))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            user = User.query.filter_by(email=form.email.data).first()
            if ph.verify(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

# takes the user email and hashes the password then stores in a 
# sqlite3 database
@app.route('/register', methods=('POST', 'GET'))
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = ph.hash(form.password.data)
        existing_user_email = User.query.filter_by(email=form.email.data).first()
        if existing_user_email:
            return abort(403)
        else:
            addusertodb(form.email.data, hashed_password)
            return redirect(url_for('login'))

    return render_template('register.html', form=form)

# as long as it's not imported as a module
# run the applicatoin on port 5000 and enable debug option
# and allow all ip addresses on the local network to request to the 
# site
if __name__ == "__main__":
    app.run(port=8000, debug=True, host='0.0.0.0')