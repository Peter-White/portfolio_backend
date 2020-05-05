from app import app, db, login
from flask import render_template, url_for, redirect, flash, session, json, jsonify, request
from app.forms import LoginForm, RegisterForm, AddSkillForm, AddProjectForm, ProjectImageForm, ProjectVideoForm
from app.models import User, Skill, Project, ProjectSkill, ProjectImage, Employee, ProjectVideo
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
    if current_user.is_authenticated:

        form = AddSkillForm()
        skills = Skill.query.all()
        if form.validate_on_submit():
            try:
                skill = Skill(
                    title = form.title.data,
                    year_started = form.year_started.data,
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
    if current_user.is_authenticated:
        projects = Project.query.all()
        return render_template('projects.html', projects=projects)
    else:
        return redirect(url_for('backLogin'))

@app.route('/projects/<int:id>', methods=['GET', 'POST'])
def project(id):
    if current_user.is_authenticated:
        imageForm = ProjectImageForm()
        videoForm = ProjectVideoForm()
        project = Project.query.filter_by(id = id).first()
        images = ProjectImage.query.filter_by(project_id = id).all()
        videos = ProjectVideo.query.filter_by(project_id = id).all()

        skills = {
            "language": [],
            "environment": [],
            "tool": [],
            "platform": [],
            "library": [],
            "database": [],
            "expertise": [],
            "framework": []
        }

        projectSkills = ProjectSkill.query.filter_by(project_id = id).all()
        for ps in projectSkills:
            skill = Skill.query.get(ps.skill_id)
            skills[skill.category].append(skill)

        if imageForm.validate_on_submit():
            try:
                data = imageForm.image.data
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

                pImage = ProjectImage(project_id = id, image = str)

                os.remove(path)

                db.session.add(pImage)
                db.session.commit()

                flash("Image posted")
                return redirect(url_for('project', id=id))
            except:
                flash("Couldn't post project image")
                return redirect(url_for('project', id=id))

        if videoForm.validate_on_submit():
            try:
                data = videoForm.video.data

                path = os.path.join(
                    app.root_path, 'static', 'videos'
                )

                i = 1
                name = data.filename
                while True:
                    name = f"{i}_{data.filename}"

                    if os.path.exists(f"{path}\\{name}"):
                        i += 1
                    else:
                        break

                path = os.path.join(
                    path, name
                )

                data.save(path)

                pVideo = ProjectVideo(project_id=id, name=name, type=data.content_type)

                db.session.add(pVideo)
                db.session.commit()

                flash("Video posted")
                return redirect(url_for('project', id=id))

            except:
                flash("Couldn't post project video")
                return redirect(url_for('project', id=id))

        return render_template('project.html', project=project, skills=skills, images=images, videos=videos, imageForm=imageForm, videoForm=videoForm)

    else:
        return redirect(url_for('backLogin'))

@app.route('/createproject', methods=['GET', 'POST'])
def createImage():
    if current_user.is_authenticated:

        form = AddProjectForm()
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

                skillData = form.language.data + form.library.data + form.platform.data + form.database.data + form.environment.data + form.framework.data + form.tool.data

                db.session.add(project)
                db.session.commit()

                projectId = project.id

                for skillId in skillData:
                    projectSkill = ProjectSkill(project_id = projectId, skill_id = skillId)

                    db.session.add(projectSkill)
                    db.session.commit()

                return redirect(url_for('projects'))
            except:
                flash("Didn't post project")
                return redirect(url_for('projects'))

        return render_template('create_project.html', form=form)
    else:
        return redirect(url_for('backLogin'))

@app.route('/editproject/<int:id>', methods=['GET', 'POST'])
def editProject(id):
    if current_user.is_authenticated:
        try:
            project = Project.query.get(id)
            form = AddProjectForm()

            dbData = {
                "title": project.title,
                "description": project.description,
                "url": project.url,
                "github": project.github,
                "language": [],
                "environment": [],
                "tool": [],
                "platform": [],
                "library": [],
                "database": [],
                "expertise": [],
                "framework": []
            }

            projectSkills = ProjectSkill.query.filter_by(project_id = id).all()
            for ps in projectSkills:
                skill = Skill.query.get(ps.skill_id)
                dbData[skill.category].append(str(skill.id))

            form.title.data = dbData["title"]
            form.description.data = dbData["description"]
            form.url.data = dbData["url"]
            form.github.data = dbData["github"]
            form.language.data = dbData["language"]
            form.library.data = dbData["library"]
            form.platform.data = dbData["platform"]
            form.database.data = dbData["database"]
            form.environment.data = dbData["environment"]
            form.framework.data = dbData["framework"]
            form.tool.data = dbData["tool"]

            if form.validate_on_submit():
                newData = {}
                newData["title"] = request.form["title"]
                newData["description"] = request.form["description"]
                newData["url"] = request.form["url"]
                newData["github"] = request.form["github"]
                newData["language"] = request.form.getlist("language")
                newData["library"] = request.form.getlist("library")
                newData["platform"] = request.form.getlist("platform")
                newData["database"] = request.form.getlist("database")
                newData["environment"] = request.form.getlist("environment")
                newData["framework"] = request.form.getlist("framework")
                newData["tool"] = request.form.getlist("tool")

                project.title = request.form["title"]
                project.description = request.form["description"]
                project.url = request.form["url"]
                project.github = request.form["github"]

                if dbData["language"] != request.form.getlist("language"):
                    for id in dbData["language"]:
                        if id not in newData["language"]:
                            db.session.delete(ProjectSkill.query.filter_by(skill_id=id, project_id=project.id).first())

                    for id in newData["language"]:
                        if ProjectSkill.query.filter_by(skill_id=id, project_id=project.id).first() == None:
                            db.session.add(ProjectSkill(project_id=project.id, skill_id=id))

                if dbData["library"] != request.form.getlist("library"):
                    for id in dbData["library"]:
                        if id not in newData["library"]:
                            db.session.delete(ProjectSkill.query.filter_by(skill_id=id, project_id=project.id).first())

                    for id in newData["library"]:
                        if ProjectSkill.query.filter_by(skill_id=id, project_id=project.id).first() == None:
                            db.session.add(ProjectSkill(project_id=project.id, skill_id=id))

                if dbData["platform"] != request.form.getlist("platform"):
                    for id in dbData["platform"]:
                        if id not in newData["platform"]:
                            db.session.delete(ProjectSkill.query.filter_by(skill_id=id, project_id=project.id).first())

                    for id in newData["platform"]:
                        if ProjectSkill.query.filter_by(skill_id=id, project_id=project.id).first() == None:
                            db.session.add(ProjectSkill(project_id=project.id, skill_id=id))

                if dbData["database"] != request.form.getlist("database"):
                    for id in dbData["database"]:
                        if id not in newData["database"]:
                            db.session.delete(ProjectSkill.query.filter_by(skill_id=id, project_id=project.id).first())

                    for id in newData["database"]:
                        if ProjectSkill.query.filter_by(skill_id=id, project_id=project.id).first() == None:
                            db.session.add(ProjectSkill(project_id=project.id, skill_id=id))

                if dbData["environment"] != request.form.getlist("environment"):
                    for id in dbData["environment"]:
                        if id not in newData["environment"]:
                            db.session.delete(ProjectSkill.query.filter_by(skill_id=id, project_id=project.id).first())

                    for id in newData["environment"]:
                        if ProjectSkill.query.filter_by(skill_id=id, project_id=project.id).first() == None:
                            db.session.add(ProjectSkill(project_id=project.id, skill_id=id))

                if dbData["framework"] != request.form.getlist("framework"):
                    for id in dbData["framework"]:
                        if id not in newData["framework"]:
                            db.session.delete(ProjectSkill.query.filter_by(skill_id=id, project_id=project.id).first())

                    for id in newData["framework"]:
                        if ProjectSkill.query.filter_by(skill_id=id, project_id=project.id).first() == None:
                            db.session.add(ProjectSkill(project_id=project.id, skill_id=id))

                if dbData["tool"] != request.form.getlist("tool"):
                    for id in dbData["tool"]:
                        if id not in newData["tool"]:
                            db.session.delete(ProjectSkill.query.filter_by(skill_id=id, project_id=project.id).first())

                    for id in newData["tool"]:
                        if ProjectSkill.query.filter_by(skill_id=id, project_id=project.id).first() == None:
                            db.session.add(ProjectSkill(project_id=project.id, skill_id=id))

                db.session.commit()
                return redirect(url_for('project', id=project.id))

        except:
            flash("Didn't edit project")
            return redirect(url_for('project', id=id))

        return render_template('edit_project.html', form=form)
    else:
        return redirect(url_for('backLogin'))

@login_required
@app.route('/deleteproject/<int:id>')
def deleteProject(id):
    pImages = ProjectImage.query.filter_by(project_id = id).all()
    pSkills = ProjectSkill.query.filter_by(project_id = id).all()

    for image in pImages:
        db.session.delete(image)

    for skill in pSkills:
        db.session.delete(skill)

    project = Project.query.get(id);
    db.session.delete(project)
    db.session.commit()

    return redirect(url_for('projects'))

@login_required
@app.route('/deleteskill', methods=['GET','POST'])
def deleteSkill():
    # try:
    id = request.args["id"]
    skill = Skill.query.filter_by(id = id).first()

    for ps in ProjectSkill.query.fileter_by(roject_id = id).all():
        db.session.delete(ps)

    db.session.delete(skill)
    db.session.commit()

    return jsonify({"success": id})
    # except:
        # return jsonify({"failed": "didn't work"})

@app.route('/deleteimage/<int:id>', methods=['GET', 'POST'])
def deleteImage(id):
    try:
        pImage = ProjectImage.query.get(id)

        db.session.delete(pImage)
        db.session.commit()

        print("image deleted")
    except:
        print("Something went wrong")

    return redirect(url_for('projects'))

@app.route('/deletevideo/<int:id>', methods=['GET', 'POST'])
def deleteVideo(id):
    try:
        pVideo = ProjectVideo.query.get(id)

        path = os.path.join(
            app.root_path, 'static', 'videos', pVideo.name
        )

        if(os.path.exists(path)):
            os.remove(path)

        db.session.delete(pVideo)
        db.session.commit()

        print("video deleted")
    except:
        print("Something went wrong")

    return redirect(url_for('projects'))

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

@app.route('/users', methods=['GET', 'POST'])
def users():
    if current_user.is_authenticated:
        return render_template('users.html')
    else:
        return redirect(url_for('backLogin'))

@app.route('/login', methods=['GET', 'POST'])
def backLogin():
    form = LoginForm()
    errors = []

    # if user is already logged in , send them to the profile page
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        # query the database for the user trying to log in
        user = User.query.filter_by(email=form.email.data).first()

        if(user != None):
            employee = Employee.query.filter_by(user_id=user.id).first()

            if employee == None:
                errors.append("Employee not found")
            elif not user.check_password(form.password.data):
                errors.append("Password does not match")
            elif not employee.confirmed:
                errors.append("Employee not confirmed")
            elif employee.role_id == 4:
                errors.append("Employees only")

            if len(errors) < 1:
                login_user(user, remember = form.remember_me.data)
                return redirect(url_for('index'))
        else:
            errors.append("User not found")

    return render_template('login.html', title="Login", form=form, errors=errors)

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
            user = User(first_name=form.first_name.data, last_name=form.last_name.data, company=form.company.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            userId = user.id
            employee = Employee(user_id = userId, role_id = 3, confirmed = False)
            db.session.add(employee)
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

        user = User(first_name=data["first_name"], last_name=data["last_name"], company=data["company"], email=data["email"])
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()



        return jsonify({ "success" : "User {} created".format(data['email']) })
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
            user = User.query.filter_by(email=data["email"]).first()

        if user:
            userJSON["id"] = user.id
            userJSON["first_name"] = user.first_name
            userJSON["last_name"] = user.last_name
            userJSON["company"] = user.company
            userJSON["email"] = user.email

        return jsonify(userJSON)
    except:
        return jsonify({"Error" : "Could not retrieve user"})

@app.route('/api/projects', methods=["GET"])
def getProjects():
    try:
        projects = Project.query.all()
        data = []

        for project in projects:
            proj = {}
            proj["id"] = project.id
            proj["title"] = project.title
            proj["url"] = project.url
            proj["description"] = project.description
            proj["github"] = project.github


            data.append(proj)

        return jsonify(data)
    except:
        return jsonify({"Error" : "Could not retrieve projects"})

@app.route('/api/projects/<int:id>', methods=["GET"])
def getProject(id):
    try:
        data = {}

        project = Project.query.filter_by(id = id).first()
        data["id"] = project.id
        data["title"] = project.title
        data["url"] = project.url
        data["description"] = project.description
        data["github"] = project.github

        data["images"] = []
        images = ProjectImage.query.filter_by(project_id = id).all()
        for image in images:
            data["images"].append({ "id" : int(image.id), "image" : str(image.image) })

        data["videos"] = []
        videos = ProjectVideo.query.filter_by(project_id = id).all()
        for video in videos:
            data["videos"].append({ "id" : int(video.id), "name" : str(video.name), "type" : str(video.type) })

        data["skills"] = {
            "language": [],
            "environment": [],
            "tool": [],
            "platform": [],
            "library": [],
            "database": [],
            "framework": []
        }

        projectSkills = ProjectSkill.query.filter_by(project_id = id).all()
        for ps in projectSkills:
            skill = Skill.query.get(ps.skill_id)
            data["skills"][skill.category].append({ "id" : int(skill.id), "title" : str(skill.title) })

        return jsonify(data)
    except:
        return jsonify({"Error" : "Could not retrieve project"})
