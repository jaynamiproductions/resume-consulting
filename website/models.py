from . import db
from flask_login import UserMixin
import datetime


class Resume(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    resume_name = db.Column(db.String(150))
    resume_data = db.Column(db.LargeBinary)
    update = db.Column(db.String(50), default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class ClientInfo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    desired_field = db.Column(db.String(150))
    highest_level_edu = db.Column(db.String(150))
    school = db.Column(db.String(150))
    major = db.Column(db.String(150))
    residence_state = db.Column(db.String(150))
    update = db.Column(db.String(50), default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    resumes = db.relationship('Resume')
    client_infos = db.relationship('ClientInfo')