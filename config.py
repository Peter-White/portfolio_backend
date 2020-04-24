import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'theressomethingaboutyouboy'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or 'postgres://hbehwdpavtlxhe:6c3ccdc394e52fd1a40ceec28a9c87d5f3590a27a07feeec35c2cfa47cc32766@ec2-54-225-116-36.compute-1.amazonaws.com:5432/dc6170jsiog6en'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or 'postgresql://postgres:ResidentEvil4@localhost:5432/portfolio'
