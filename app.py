from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///relations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)

# ONE TO ONE
class User(db.Model):
    # __tablename__ = 'Users': there is no need to add this
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),nullable=False)
    profile = db.relationship('Profile',back_populates='user', uselist=False)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    user = db.relationship('User', back_populates='profile')

class TeamManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    students = db.relationship('Student', back_populates='team_manager')

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    team_manager_id = db.Column(db.Integer, db.ForeignKey('team_manager.id'))
    team_manager = db.relationship('TeamManager', back_populates='students')

# JOIN TABLE
enrollment = db.Table(
    'enrollment',
    db.Column('learner_id', db.Integer,db.ForeignKey('learner.id'),primary_key=True),
    db.Column('course_id',db.Integer,db.ForeignKey('course.id'),primary_key=True)
)

class Learner(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(45),nullable=False)
    courses = db.relationship('Course',secondary=enrollment,back_populates='learners')

class Course(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50),nullable = False)
    learners = db.relationship('Learner',secondary=enrollment,back_populates = 'courses')