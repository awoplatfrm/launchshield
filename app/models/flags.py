from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
    UniqueConstraint,
    Integer,
    Boolean,
)
from sqlalchemy.orm import relationship, mapped_column, Mapped
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from app.models.tenants import db


class FeatureFlag(db.Model):

    __tablename__ = "feature_flags"
    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    tenant_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenants.id"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (UniqueConstraint("tenant_id", "key", name="uq_tenant_flag_key"),)


def __repr__(self) -> str:
    return f"<FeatureFlag key='{self.key}' enabled={self.is_enabled}>"
