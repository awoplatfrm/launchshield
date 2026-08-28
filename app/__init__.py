from flask import Flask, request, render_template, make_response, jsonify
from app.config import config_by_name
from app.models.users import User
from app.models.tenants import Tenant, db
from app.models.flags import FeatureFlag
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app(config_name="development", config_override=None):

    app = Flask(__name__, instance_relative_config=True)
    # config app
    # load configuration class

    cls_config = config_by_name.get(config_name, config_by_name["development"])
    app.config.from_object(cls_config)

    if config_override:
        app.config.update(config_override)

    # initialize db AFTER config applied
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):

        return db.session.get(User, int(user_id))

    # register route blueprint
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/api/v1")
    app.register_blueprint(api_bp, url_prefix="/api/v1/flags")

    # database schema initialization
    with app.app_context():
        db.create_all()

    @app.route("/health")
    def health_check():
        return {"status": "healthy", "app_name": "launchshield"}

    return app
