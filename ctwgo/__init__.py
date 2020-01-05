import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from ctwgo.config import Config 



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# specify login route locatio
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


############################################################################################
def create_app(config_class=Config):
    current_path = os.path.abspath(__file__)
    static_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")

    app = Flask(__name__, static_url_path= static_path + "/static")
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from ctwgo.users.routes import users
    from ctwgo.posts.routes import posts
    from ctwgo.main.routes import main
    from ctwgo.errors.handlers import errors
    from ctwgo.comments.routes import comments
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(comments)

    ## Only this code when first time create database
    # with app.app_context():
    #     db.create_all()

    return app

