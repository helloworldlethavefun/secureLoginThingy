from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf.file import FileRequired, FileField
from database import User

# Setup the register form for creating a new user.
# Also inclueds a function for checking if the user
# that is being created already exists in the db
class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=100)], render_kw={'placeholder': 'email'})
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=100)], render_kw={'placeholder': 'password'})
    submit = SubmitField('Regsiter')

    def validateemail(email):
        existing_user_email = User.query.filter_by(email=email).first()
        if existing_user_email:
            raise ValidationError()

# Creates a login form
class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=100)], render_kw={'placeholder': 'email'})
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=100)], render_kw={'placeholder': 'password'})
    submit = SubmitField('Login')

# This is for getting the email of the user so we can
# send the reset link
class ResetPasswordEmail(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=100)], render_kw={'placeholder': 'email'})
    submit = SubmitField('Send reset link')

# Actually changing the password
class ResetPassword(FlaskForm):
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=100)], render_kw={'placeholder': 'password'})
    submit = SubmitField('Change password')

# File upload form as it's named
class UploadForm(FlaskForm):
    file = FileField(validators=[FileRequired()])