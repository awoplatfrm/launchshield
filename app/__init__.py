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


def create_app(config_name="development"):

    app = Flask(__name__, instance_relative_config=True)
    # config app
    # load configuration class
    app.config.from_object(
        config_by_name.get(config_name, config_by_name["development"])
    )
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):

        return db.session.get(User, int(user_id))

    # register route blueprint
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/api/v1")

    # database schema initialization
    with app.app_context():
        db.create_all()

    @app.route("/health")
    def health_check():
        return {"status": "healthy", "app_name": "launchshield"}

    @app.get("/api/v1/flags/evaluate")
    def evaluate_flag():
        tenant = request.args.get("tenant", "public")
        flag_name = request.args.get("flag", "default_flag")

        return {
            "tenant": tenant,
            "flag": flag_name,
            "enable": True,
            "reason": "targeting rule matched",
        }

    @app.get("/api/v1/tenants/<int:tenant_id>")
    def get_tenant(tenant_id):
        return {
            "tenant_id": tenant_id,
            "company_name": f"Tenant_{tenant_id} Corp",
            "tier": "Pro Plan",
        }

    @app.post("/api/v1/flags/create")
    def create_flag():
        header = request.headers.get("X-API-KEY")
        if not header:
            return {"error": " Missing X-API-KEY Header"}, 401
        payload = request.get_json(silent=True)

        if not payload or "flag-key" not in payload:
            return {"error": "invalid payload. flag-key is missing"}, 400
        flag_key = payload.get("flag_key")
        is_enable = payload.get("is_enable", False)

        return {
            "status": "success",
            "message": f"Feature flag {flag_key} created successfully",
            "data": {
                "flag_key": flag_key,
                "is_enable": is_enable,
                "created_by_api_key": header,
            },
        }, 201

    return app
