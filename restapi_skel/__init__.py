from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

from .config import config_by_name

# Database
db = SQLAlchemy()

# Authentication
authentication = HTTPBasicAuth()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .tasks import tasks as tasks_blueprint
    app.register_blueprint(tasks_blueprint, url_prefix='/tasks')

    return app
