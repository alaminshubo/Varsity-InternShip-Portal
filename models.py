from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# 1. Student Table  
class Student(db.Model):
    __tablename__ = 'student_profile'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    
    university = db.Column(db.String(150), nullable=True)
    skills = db.Column(db.Text, nullable=True)
    cv = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='student', cascade="all, delete-orphan", lazy=True)
    reviews = db.relationship('Review', backref='student', cascade="all, delete-orphan", lazy=True)


# 2. Company Table  
class Company(db.Model):
    __tablename__ = 'company_profile'
    
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    description = db.Column(db.Text, nullable=True)
    website = db.Column(db.String(150), nullable=True)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    internships = db.relationship('Internship', backref='company', cascade="all, delete-orphan", lazy=True)
    reviews = db.relationship('Review', backref='company', cascade="all, delete-orphan", lazy=True)


# 3. Admin Table  
class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# 4. Internship Post Table
class Internship(db.Model):
    __tablename__ = 'internships'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company_profile.id', ondelete='CASCADE'), nullable=False)
    
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))
    location = db.Column(db.String(100))
    deadline = db.Column(db.Date)
    status = db.Column(db.Enum('pending', 'approved', 'rejected', name='internship_status'), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='internship', cascade="all, delete-orphan", lazy=True)


# 5. Student Apply Table
class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    internship_id = db.Column(db.Integer, db.ForeignKey('internships.id', ondelete='CASCADE'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profile.id', ondelete='CASCADE'), nullable=False)
    
    status = db.Column(db.Enum('pending', 'accepted', 'rejected', name='application_status'), default='pending')
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)


# 6. Review System Table
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company_profile.id', ondelete='CASCADE'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profile.id', ondelete='CASCADE'), nullable=False)
    
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# 7. Admin Report Table
class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    reporter_type = db.Column(db.Enum('student', 'company', name='reporter_types'), nullable=False)
    reporter_id = db.Column(db.Integer, nullable=False) 
    
    report_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
