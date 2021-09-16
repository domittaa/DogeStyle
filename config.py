import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))  # import .env file


class Config(object):  # os.environ.get- sources from an enviroment variable
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')  # if the email server is not set in environment, the emailing errors needs to be disabled
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None  # not used by default
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['klodzinska.d@gmail.com']
    POSTS_PER_PAGE = 5
    COMMENTS_PER_PAGE = 10
    UPLOAD_PATH = 'app/static/files'
    UPLOAD_AVATAR_PATH = 'app/static/avatars'
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif']
    MAX_CONTENT_LENGTH = 1024 * 1024
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')



