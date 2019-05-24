# importing Flask class from flask.py file
from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# create an instance of the Flash class, in order to run this application
# name parameter will default to folder name
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)

# you have to instatiate the database variables after the config has been set
# reason is that the config holds the location of the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# app variables for login
login = LoginManager(app)

# when a page requires somebody to logged in, the application will by default send them back to the previous page, however we will make them go back to the login instead
login.login_view = 'login'

# from the app folder, import the routes.py file, and startup at the index route
from app import routes
