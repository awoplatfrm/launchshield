import uuid  # noqa: I001
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    String,
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

db = SQLAlchemy()


class Tenant(db.Model):
    __tablename__ = "tenants"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    api_key = Column(
        String(64),
        nullable=False,
        unique=True,
        default=lambda: f"ls_live_{uuid.uuid4().hex}",
    )
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    users = relationship(
        "User", backref="tenant", lazy=True, cascade="all, delete-orphan"
    )
    feature_flag = relationship(
        "FeatureFlag", backref="flag", lazy=True, cascade="all, delete-orphan"
    )
