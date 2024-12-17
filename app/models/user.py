from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # Hashowanie hasła
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Weryfikacja hasła
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)