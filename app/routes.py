from app import app, db, login
from flask import render_template, url_for, redirect, flash, session, json, jsonify, request
from app.forms import CommandInput, LoginForm, RegisterForm, AddSkillForm
from app.models import User, Skill
from flask_login import current_user, login_user, logout_user, login_required
import jwt
from sqlalchemy import or_

# create route for index page, render index.html file
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/skills')
def skills():
    form = AddSkillForm()
    skills =

@app.route('/api/register', methods=['GET','POST'])
def register():
    try:
        token = request.headers.get('token')

        # decode the token back to a dictionary
        data = jwt.decode(
            token,
            app.config["SECRET_KEY"],
            algorithm=["HS256"]
        )

        user = User(first_name=data["first_name"], last_name=data["last_name"], company=data["company"], username=data["username"], email=data["email"])
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()

        return jsonify({ "success" : "User {} created".format(data['username']) })
    except:
        return jsonify({ "error": "Failed to create user" })

@app.route('/api/login', methods=['GET','POST'])
def login():
    try:
        token = request.headers.get('token')

        data = jwt.decode(
            token,
            app.config["SECRET_KEY"],
            algorithm=["HS256"]
        )

        user = User.query.filter_by(email=data["email"]).first()

        if user is None or not user.check_password(data["password"]):
            return jsonify({ "message": 'Error #002: Invalid credentials' })

        return jsonify({ 'message': 'success', 'token': user.get_token() })

    except:
        return jsonify({ "error" : "failed to login" })

@app.route('/api/users', methods=["GET"])
def getUsers():
    try:
        users = User.query.all()
        usersJSON = []

        for user in users:
            usersJSON.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "company": user.company,
                "username": user.username,
                "email": user.email,
                "password_hash": user.password_hash
            })

        return jsonify(usersJSON)
    except:
        return jsonify({ "Error": "Cannot retrieve users" })

@app.route('/api/user', methods=["GET"])
def getUser():
    try:
        token = request.headers.get('token')

        # decode the token back to a dictionary
        data = jwt.decode(
            token,
            app.config["SECRET_KEY"],
            algorithm=["HS256"]
        )

        userJSON = {}

        if "user_id" in data:
            user = User.query.filter_by(id = data["user_id"]).first()
        else:
            user = User.query.filter(or_(User.email == data["email"], User.username == data["username"])).first()

        if user:
            userJSON["id"] = user.id
            userJSON["first_name"] = user.first_name
            userJSON["last_name"] = user.last_name
            userJSON["company"] = user.company
            userJSON["username"] = user.username
            userJSON["email"] = user.email

        return jsonify(userJSON)
    except:
        return jsonify({"Error" : "Could not retrieve user"})
