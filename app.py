# import needed modules
from flask import Flask, render_template, redirect, url_for, request, session, abort
from argon2 import PasswordHasher, Type
from argon2.exceptions import VerificationError
from database import db, User, addusertodb
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from form import LoginForm, RegisterForm, ValidationError

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# just the index route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    print(current_user)
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

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

# if posted to request to view the posted info then store in a variable
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

    return render_template('register.html', form=form)

# as long as it's not imported as a module
# run the applicatoin on port 5000 and enable debug
if __name__ == "__main__":
    app.run(port=8000, debug=True, host='0.0.0.0')