"""Plans and Service related models and database functionality"""
import uuid
from sqlalchemy.dialects.postgresql import ENUM

from flask import current_app
from sqlalchemy import and_, or_
from sqlalchemy.dialects.postgresql import ARRAY
from src.models.base import db

# Join table for Subscription and ServiceCode
subscriptions_service_codes = db.Table(
    "subscriptions_service_codes", db.Model.metadata,
    db.Column("subscription_id", db.Integer,
              db.ForeignKey("subscriptions.id"), primary_key=True),
    db.Column("service_code_id", db.Integer,
              db.ForeignKey("service_codes.id"), primary_key=True)
)


class Plan(db.Model):
    """Model class to represent mobile service plans"""
    __tablename__ = "plans"
    id = db.Column(db.String(30), primary_key=True)
    description = db.Column(db.String(200))
    # amount of data available for a given billing cycle
    mb_available = db.Column(db.BigInteger)
    is_unlimited = db.Column(db.Boolean)

    def __repr__(self):  # pragma: no cover
        return (
            f"<{self.__class__.__name__}: {self.id} ({self.description})>"
        )


class ServiceCode(db.Model):
    """Model class to represent service codes"""

    __tablename__ = "service_codes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    version = db.relationship("ServiceCodeVersions", uselist=False)

    subscriptions = db.relationship(
        "Subscription", secondary=subscriptions_service_codes,
        primaryjoin="ServiceCode.id==subscriptions_service_codes.c.service_code_id",
        secondaryjoin="Subscription.id==subscriptions_service_codes.c.subscription_id",
        back_populates="service_codes", cascade="all,delete",
    )

    def __repr__(self):  # pragma: no cover
        return (
            f"<{self.__class__.__name__}: {self.id}, "
            f"{self.name}: ({self.description})>"
        )

    @classmethod
    def get_data_blocking_code(cls):
        """Gets the data blocking service code"""
        return cls.get_one(name=cls.get_data_blocking_code_name())

    @classmethod
    def get_data_blocking_code_name(cls):
        """Gets the name of the data blocking service code"""
        return current_app.config.get("DATA_BLOCKING_CODE")

    @classmethod
    def get_one(cls, name):
        return ServiceCode.query.filter_by(name=name).first()


class ServiceCodeVersions(db.Model):

    __tablename__ = "service_code_versions"

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(), nullable=False, default=uuid.uuid4())
    from_date = db.Column(db.TIMESTAMP(timezone=True))
    status = db.Column(ENUM('added', 'remove'), default='added')

    service_code_id = db.Column(db.Integer, db.ForeignKey("service_codes.id"), nullable=False)
    service_code = db.relationship("ServiceCode", foreign_keys=[service_code_id], lazy="select")

    subscription_id = db.Column(db.Integer, db.ForeignKey("subscriptions.id"), nullable=False)
    subscription = db.relationship("Subscription", foreign_keys=[subscription_id], lazy="select")
