from datetime import datetime
from flask import current_app
from habit_app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    habits = db.relationship('Habit', backref='user', lazy=True)

    def __repr__(self):
        return f"User: {self.name}, {self.email}"


class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(), nullable=False)
    time_spent = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Habit: {self.activity} FOR {self.time_spent}. Created: {self.created_at}"