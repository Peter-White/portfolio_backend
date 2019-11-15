from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, TextAreaField, BooleanField, RadioField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, length, ValidationError
from app.models import User, Skill
from flask import flash

def skills(category):
    skills = Skill.query.filter_by(category = category).all()
    skillArr = []

    for skill in skills:
        skillArr.append(('{}'.format(skill.id), '{}'.format(skill.title)))

    return skillArr

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    company = StringField("Company Name")
    username = StringField("Username", validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

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

class AddSkillForm(FlaskForm):
    title = StringField("Skill Title")
    yearStarted = IntegerField('Year Started')
    category = RadioField('Category', choices=[('language', 'Language'), ('framework', 'Framework'), ('database', 'Database Tools'), ('tool','Tool'), ('library', 'Library'), ('environment', 'Environment'), ('expertise','Expertise ')])
    submit = SubmitField('Submit')

class AddProjectForm(FlaskForm):
    title = StringField("Project Title")
    description = TextAreaField("Project Description", validators=[DataRequired(), length(max=1000)])
    url = StringField("URL")
    github = StringField("GitHub URL")
    language = SelectMultipleField('Languages Used', choices=skills("language"))
    library = SelectMultipleField('Libraries Used', choices=skills("library"))
    database = SelectMultipleField('Databases Used', choices=skills("database"))
    environment = SelectMultipleField('Environments Used', choices=skills("environment"))
    framework = SelectMultipleField('Frameworks Used', choices=skills("framework"))
    tool = SelectMultipleField('Tools Used', choices=skills("tool"))
    submit = SubmitField('Submit')
