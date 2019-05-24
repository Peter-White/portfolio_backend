from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, length, ValidationError
from app.models import User
from flask import flash

class CommandInput(FlaskForm):
    command = StringField("C:/>")

class LoginForm(FlaskForm):
    email = StringField('Electronic Super Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    company = StringField("Company Name")
    username = StringField("Username", validators=[DataRequired()])
    email = StringField('Electronic Super Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            flash('Sorry but those credentials are already in use')
            raise ValidationError('Use a different username/email.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            flash('Sorry but those credentials are already in use')
            raise ValidationError('Use a different username/email.')
