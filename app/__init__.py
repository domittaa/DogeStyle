from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
import os

# create extension instances in the global scope with no arguments passed to it
# it is not attached to the application yet
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()


def create_app(config_class=Config):  # creates Flask application instance
    app = Flask(__name__)
    app.config.from_object(config_class)

    # bind extension instances to  application
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')  # adds auth to url in this blueprint

    from app.user import bp as user_bp
    app.register_blueprint(user_bp)

    from app.post import bp as post_bp
    app.register_blueprint(post_bp)

# python use logging package to write its logs and this package has the ability to send logs by email
# to do this we need to add a SMTPHandler instance to the Flask logger object- app.logger

    if not app.debug and not app.testing:  # enable email logger only if app is running without debug mode, skip logging during tests
        if app.config['MAIL_SERVER']:  # enable email logger only if email server exists in config
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(  # creates a SMTPHandler instance
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject="Microblog Failure",
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)  # set level to only report errors and not warnings, messages etc
            app.logger.addHandler(mail_handler)  # attach SMTPHandler instance to the app.logger object from Flask
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
# enable a file based log another handler- of type RotatingFileHandler
            if not os.path.exists('logs'):  # creates the log file microblog.log in logs directory,
                os.mkdir('logs')            # which is created if it doesnt already exists
            file_handler = RotatingFileHandler(
                'logs/microblog.log', maxBytes=10240, backupCount=10
            )  # ensures that the log file do not grow too large
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))   # custom formatting log messages
            file_handler.setLevel(logging.INFO)  # set logging level to INFO
        # logging categories in increasing order of severity are: DEBUG, INFO, WARNING, ERROR, CRITICAL
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app


from app import models
