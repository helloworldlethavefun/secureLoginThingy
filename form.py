from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from database import User

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'password'})
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'password'})
    submit = SubmitField('Regsiter')

    def validateusername(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "This username already exists please enter a different one!"
            )


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'password'})
    password = PasswordField('password', validators=[InputRequired, Length(min=4, max=20)], render_kw={'placeholder': 'password'})
    submit = SubmitField('Login')