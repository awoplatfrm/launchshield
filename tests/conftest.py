import pytest
from app.models.tenants import db as _db
from app.models.flags import FeatureFlag
from app.models.tenants import Tenant
from app import create_app


@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "WTF_CSRF_ENABLED": False,
    }
    app = create_app(config_name="testing", config_override=test_config)

    with app.app_context():
        _db.create_all()

        test_tenant = Tenant(id="tenant_123", name="acne corp")
        test_flag = FeatureFlag(
            key="new_landing_page",
            name="New Landing Page",
            is_enabled=True,
            tenant_id="tenant_123",
        )

        _db.session.add(test_tenant)
        _db.session.add(test_flag)

        _db.session.commit()
        yield app

        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
