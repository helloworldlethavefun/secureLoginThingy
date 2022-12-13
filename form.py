from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from database import User

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=100)], render_kw={'placeholder': 'email'})
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=100)], render_kw={'placeholder': 'password'})
    submit = SubmitField('Regsiter')

    def validateemail(email):
        existing_user_email = User.query.filter_by(email=email).first()
        if existing_user_email:
            raise ValidationError()


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=100)], render_kw={'placeholder': 'email'})
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=100)], render_kw={'placeholder': 'password'})
    submit = SubmitField('Login')

class ResetPassword(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=100)], render_kw={'placeholder': 'email'})
    submit = SubmitField('Send reset code')