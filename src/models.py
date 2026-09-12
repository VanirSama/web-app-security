from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, UTC
from bcrypt import hashpw, gensalt, checkpw

db = SQLAlchemy()


class UserModel(UserMixin, db.Model):
    __tablename__   = 'users'
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username        = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash   = db.Column(db.String(255), nullable=False)

    notes           = db.relationship("NoteModel", backref="author", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password_hash = hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))


class NoteModel(db.Model):
    __tablename__ = 'notes'
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title       = db.Column(db.String(200), nullable=False)
    content     = db.Column(db.Text, nullable=False)
    created_at  = db.Column(db.DateTime(timezone=True), default=datetime.now()) # default=datetime.now(UTC)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
