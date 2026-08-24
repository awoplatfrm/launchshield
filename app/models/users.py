from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import datetime
from uuid import uuid4
from app.models.tenants import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    is_admin = Column(Boolean, default=False)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False)
