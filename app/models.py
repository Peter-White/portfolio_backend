from app import app, db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(50))
    username = db.Column(db.String(30), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=86400):
        return jwt.encode(
            { 'user_id': self.id, 'exp': time() + expires_in },
            app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_token(token):
        try:
            id = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithm=['HS256']
            )["user_id"]
        except:
            return

        return User.query.get(id)

    def __repr__(self):
        return '<User {}>'.format(self.email)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    url = db.Column(db.String(500), unique=True, nullable=True)
    description = db.Column(db.String(1000), nullable=False)
    github = db.Column(db.String(500), unique=True, nullable=True)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    yearStarted = db.Column(db.Integer, nullable=False)

class ProjectSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projectID = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    skillID = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)

class ProjectImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projectID = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
