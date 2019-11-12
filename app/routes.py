from app import app, db, login
from flask import render_template, url_for, redirect, flash, session, json, jsonify, request
from app.forms import LoginForm, RegisterForm, AddSkillForm, AddProjectForm
from app.models import User, Skill, Project, ProjectSkill
from flask_login import current_user, login_user, logout_user, login_required
import jwt
from sqlalchemy import or_

# ********************************************************************************
# Secret Backend Pages
# ********************************************************************************

@app.route('/')
@app.route('/index')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('backLogin'))

    return render_template('index.html', title="Mistah White")

@app.route('/skills', methods=['GET', 'POST'])
def skills():
    form = AddSkillForm()
    skills = Skill.query.all()

    if current_user.is_authenticated:
        if form.validate_on_submit():
            try:
                skill = Skill(
                    title = form.title.data,
                    yearStarted = form.yearStarted.data,
                    category = form.category.data
                )

                db.session.add(skill)
                db.session.commit()

                return redirect(url_for('skills'))
            except:
                flash("Didn't post skill")
                return redirect(url_for('skills'))

        return render_template('skills.html', skills=skills, form=form, title="Skills")
    else:
        return redirect(url_for('backLogin'))

@app.route('/projects', methods=['GET', 'POST'])
def projects():
    form = AddProjectForm()
    projects = Project.query.all()

    if current_user.is_authenticated:
        if form.validate_on_submit():
            try:
                if(form.url.data == "" and form.github.data == ""):
                    flash("One URL required")
                    return redirect(url_for('projects'))

                project = Project(
                    title = form.title.data,
                    description = form.description.data,
                    url = form.url.data,
                    github = form.github.data
                )

                db.session.add(project)
                db.session.commit()

                projectId = project.id

                skills = form.language.data + form.library.data + form.database.data + form.environment.data + form.framework.data + form.tool.data

                for skillId in skills:
                    projectSkill = ProjectSkill(projectID = projectId, skillID = skillId)

                    db.session.add(projectSkill)
                    db.session.commit()

                return redirect(url_for('projects'))
            except:
                flash("Didn't post project")
                return redirect(url_for('projects'))

        return render_template('projects.html', projects=projects, form=form)
    else:
        return redirect(url_for('backLogin'))

@app.route('/users', methods=['GET', 'POST'])
def users():
    return render_template('users.html')

@app.route('/projects/<int:id>', methods=['GET', 'POST'])
def project(id):
    if current_user.is_authenticated:
        project = Project.query.filter_by(id = id).first()

        return render_template('project.html', project=project)
    else:
        return redirect(url_for('backLogin'))

@app.route('/login', methods=['GET', 'POST'])
def backLogin():
    form = LoginForm()

    # if user is already logged in , send them to the profile page
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        # query the database for the user trying to log in
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('index'))

        login_user(user, remember = form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('login.html', title="Login", form=form)

@login_required
@app.route('/logout')
def backLogout():
    logout_user()
    return redirect(url_for('backLogin'))

@app.route('/register', methods=['GET', 'POST'])
def backRegister():
    form = RegisterForm()

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        try:
            user = User(first_name=data["first_name"], last_name=data["last_name"], company=data["company"], username=data["username"], email=data["email"])
            user.set_password(data["password"])
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('login'))
        except:
            flash("Couldn't register")
            return redirect(url_for('register'))

    return render_template('register.html', form=form, title="Register")

# ********************************************************************************
# API Routes
# ********************************************************************************

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

@app.route('/api/deleteskill', methods=['GET','POST'])
def deleteSkill():
    try:
        id = request.args["id"]
        skill = Skill.query.filter_by(id = id).first()

        db.session.delete(skill)
        db.session.commit()

        return jsonify({"success": id})
    except:
        return jsonify({"failed": "didn't work"})
