from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    last_login = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    sent_letters = db.relationship(
        "Letter",
        foreign_keys="Letter.sender_id",
        backref="sender",
        lazy=True
    )

    received_letters = db.relationship(
        "Letter",
        foreign_keys="Letter.receiver_id",
        backref="receiver",
        lazy=True
    )

    notifications = db.relationship(
        "Notification",
        backref="user",
        lazy=True
    )


class Letter(db.Model):
    __tablename__ = "letters"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    background = db.Column(
        db.String(100),
        default="sky.jpg"
    )

    is_read = db.Column(
        db.Boolean,
        default=False
    )

    reply_to = db.Column(
        db.Integer,
        db.ForeignKey("letters.id"),
        nullable=True
    )

    deleted_by_sender = db.Column(
        db.Boolean,
        default=False
    )

    deleted_by_receiver = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    message = db.Column(
        db.String(255),
        nullable=False
    )

    link = db.Column(
        db.String(255),
        nullable=False
    )

    is_read = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
