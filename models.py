from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  
db = SQLAlchemy()
# Models 
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)     
    name = db.Column(db.String(100))     
    email = db.Column(db.String(100), unique=True)     
    password_hash = db.Column(db.String(255))  
class Course(db.Model):     
    id = db.Column(db.Integer, primary_key=True)     
    title = db.Column(db.String(100))     
    description = db.Column(db.Text)  
class Enrollment(db.Model):     
    id = db.Column(db.Integer, primary_key=True)     
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))     
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))     
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  
