from datetime import datetime, timezone, timedelta
from uuid import uuid4

from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property

from flask_api import db, bcrypt
from flask_api.util.datetime_util import (
    utc_now,
    get_local_utcoffset,
    make_tzaware,
    localized_dt_string,
)

class User(db.Model):
    """User Model for interacting with user related data"""
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    registered_on = db.Column(db.DateTime, default=utc_now())
    public_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid4()))
    admin = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return (
            f"<User {self.email}, {self.registered_on}, {self.public_id}>"
        )
        
    @hybrid_property
    def registered_on_str(self):
        registered_on_utc = make_tzaware(
            self.registered_on, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(registered_on_utc, use_tz=get_local_utcoffset())
    
    
    @property    
    def password(self):
        """Prevent password from being accessed directly."""
        raise AttributeError("password is not a readable attribute")
    
    @password.setter
    def password(self, password):
        """Hash the password using bcrypt.
        :param password: The password to hash
        :return: None
        """
        log_rounds = current_app.config.get("BCRYPT_LOG_ROUNDS")
        hash_bytes = bcrypt.generate_password_hash(password, log_rounds=log_rounds)
        self.password_hash = hash_bytes.decode("utf-8")
    
    def check_password(self, password):
        """Check hashed password against provided password.
        :param password: The password to check
        :return: True if the password matches, False otherwise
        """
        return bcrypt.check_password_hash(self.password_hash, password)
    
    @classmethod
    def find_by_email(cls, email):
        """Find a user by their email address.
        :param email: The email address to search for
        :return: User object if found, None otherwise
        """
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_public_id(cls, public_id):
        """Find a user by their public ID.
        :param public_id: The public ID to search for
        :return: User object if found, None otherwise
        """
        return cls.query.filter_by(public_id=public_id).first()
    


