from flask_login import UserMixin

from sqlalchemy import Column, ForeignKey, Integer, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy_imageattach.entity import Image, image_attachment

from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    __tablename__ = 'user'

class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    organizator_id = db.Column(db.Integer, ForeignKey('user.id'))
    organizator = relationship('User')
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    # image = image_attachment('EventImage')
    image_path = db.Column(db.String(100))
    image_name = db.Column(db.String(100))
    datetime = db.Column(db.DateTime)
    __tablename__ = 'event'
    # Idopont (kezdes) pl: 2020.10.28 16:00
    # Hanyan vannak becsatlakozva
    # Resztvevok listaja (list of users)


class EventUsers(db.Model):
    event_user_id = Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, ForeignKey('event.event_id'))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    user = relationship('User')
    event = relationship('Event')
    __tablename__ = 'event_users'
