from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from habit_app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initiate extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Import and then initialize blueprints
    from habit_app.habits import habits
    from habit_app.auth import auth
    from habit_app.errors import errors
    app.register_blueprint(habits)
    app.register_blueprint(auth)
    app.register_blueprint(errors)

    return app