import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'temp'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or 'postgresql://postgres:ResidentEvil4@localhost:5432/portfolio'
