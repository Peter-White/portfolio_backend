from app import app, db, login
from flask import render_template, url_for, redirect, flash
from app.forms import CommandInput, LoginForm, RegisterForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required

# create route for index page, render index.html file
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
