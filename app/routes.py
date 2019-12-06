from app import app, db, login
from flask import render_template, url_for, redirect, flash, session, json, jsonify, request
from app.forms import LoginForm, RegisterForm, AddSkillForm, AddProjectForm, ProjectImageForm
from app.models import User, Skill, Project, ProjectSkill, ProjectImage
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from sqlalchemy import or_
import base64
import jwt
import os

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

@app.route('/projects/<int:id>', methods=['GET', 'POST'])
def project(id):
    if current_user.is_authenticated:
        form = ProjectImageForm()
        project = Project.query.filter_by(id = id).first()
        images = ProjectImage.query.filter_by(projectID = id).all()
        allSkills = Skill.query.all()

        skills = {
            "language": [],
            "environment": [],
            "tool": [],
            "library": [],
            "database": [],
            "expertise": [],
            "framework": []
        }
        otherSkills = {
            "language": [],
            "environment": [],
            "tool": [],
            "library": [],
            "database": [],
            "expertise": [],
            "framework": []
        }

        projectSkills = ProjectSkill.query.filter_by(projectID = id).all()
        for ps in projectSkills:
            skill = Skill.query.get(ps.skillID)
            skills[skill.category].append(skill)
            allSkills.remove(skill)

        for skill in allSkills:
            otherSkills[skill.category].append(skill)

        if form.validate_on_submit():
            try:
                data = form.image.data
                filename = secure_filename(data.filename)

                path = os.path.join(
                    app.instance_path, 'images'
                )

                if(not os.path.exists(path)):
                    os.makedirs(path)

                path = os.path.join(path, filename)

                data.save(path)

                str = ""
                with open(path, "rb") as imageFile:
                    str = base64.b64encode(imageFile.read())

                pImage = ProjectImage(projectID = id, image = str)

                os.remove(path)

                db.session.add(pImage)
                db.session.commit()

                flash("Image posted")
                return redirect(url_for('project', id=id))
            except:
                flash("Didn't post project")
                return redirect(url_for('project', id=id))

        return render_template('project.html', project=project, skills=skills, otherSkills=otherSkills, images=images, form=form)
    else:
        return redirect(url_for('backLogin'))

@app.route('/deleteimage/<int:id>', methods=['GET', 'POST'])
def deleteImage(id):
    try:
        pImage = ProjectImage.query.get(id)

        db.session.delete(pImage)
        db.session.commit()

        return jsonify({ "success" : "image deleted" })
    except:
        return jsonify({ "failed" : "Something went wrong" })

@app.route('/addprojectskill', methods=['GET', 'POST'])
def addProjectSkill():
    try:
        args = request.args
        skillId = int(args.get("skill"))
        projectId = int(args.get("project"))

        db.session.add(ProjectSkill(projectID=projectId, skillID=skillId))
        db.session.commit()

        skill = Skill.query.get(skillId);

        return jsonify({ "success" : {
                "id" : skill.id,
                "title" : skill.title,
                "category" : skill.category,
                "yearStarted" : skill.yearStarted
            }
        })
    except:
        return jsonify({ "failed" : "Something went wrong" })

@app.route('/deleteprojectskill', methods=['GET', 'POST'])
def deleteProjectSkill():
    try:
        args = request.args
        skillId = int(args.get("skill"))
        projectId = int(args.get("project"))

        pSkill = ProjectSkill.query.filter_by(skillID=skillId, projectID=projectId).first()

        db.session.delete(pSkill)
        db.session.commit()

        return jsonify({ "success" : "project skill deleted" })
    except:
        return jsonify({ "failed" : "Something went wrong" })

@app.route('/users', methods=['GET', 'POST'])
def users():
    if current_user.is_authenticated:
        return render_template('users.html')
    else:
        return redirect(url_for('backLogin'))

@login_required
@app.route('/deleteproject/<int:id>')
def deleteProject(id):
    pImages = ProjectImage.query.filter_by(projectID = id).all()
    pSkills = ProjectSkill.query.filter_by(projectID = id).all()

    for image in pImages:
        db.session.delete(image)

    for skill in pSkills:
        db.session.delete(skill)

    project = Project.query.get(id);
    db.session.delete(project)
    db.session.commit()

    return redirect(url_for('projects'))

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
            user = User(first_name=form.first_name.data, last_name=form.last_name.data, company=form.company.data, username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('backLogin'))
        except:
            flash("Couldn't register")
            return redirect(url_for('backRegister'))

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
