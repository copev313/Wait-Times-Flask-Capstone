from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from waittimes.config import Config


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'views.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    from waittimes.errors.handlers import errors
    from waittimes.main.routes import main
    from waittimes.auth.routes import auth
    from waittimes.admin.routes import admin
    from waittimes.rides.routes import rides
    from waittimes.waittimes.routes import waittimes
    from waittimes.tickets.routes import tickets
    app.register_blueprint(auth, url_prefix='')
    app.register_blueprint(main, url_prefix='')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(errors, url_prefix='/error')
    app.register_blueprint(rides, url_prefix='/ride')
    app.register_blueprint(waittimes, url_prefix='/waittime')
    app.register_blueprint(tickets, url_prefix='/ticket')
    
    return app
