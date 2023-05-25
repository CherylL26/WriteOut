from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, login
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(128))
    universes = db.relationship('Universe', backref='user', lazy='dynamic')
    viewable_universes = db.relationship('UPermission', backref='user', lazy='dynamic')

    def set_password(self, pw):
        self.password = generate_password_hash(pw)

    def check_password_hash(self, pw):
        return check_password_hash(self.password, pw)


class Universe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    projects = db.relationship('Project', backref='universe', lazy='dynamic')
    lore = db.relationship('Lore', backref='universe', lazy='dynamic')
    permissions = db.relationship('UPermission', backref='universe', lazy='dynamic')


class UPermission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    universe_id = db.Column(db.Integer, db.ForeignKey('universe.id'))
    viewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    edit = db.Column(db.Boolean)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    universe_id = db.Column(db.Integer, db.ForeignKey('universe.id'))
    title = db.Column(db.String(128), index=True)
    text = db.Column(db.Text)


class Lore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    universe_id = db.Column(db.Integer, db.ForeignKey('universe.id'))
    title = db.Column(db.String(120), index=True)
    text = db.Column(db.Text)
