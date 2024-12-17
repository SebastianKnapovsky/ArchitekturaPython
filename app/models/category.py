from app import db
from flask_login import current_user

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expenses = db.relationship('Expense', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"