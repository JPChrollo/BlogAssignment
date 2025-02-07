

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from blogapp import db

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(
        db.String(20), nullable=False, default="default_profile.png"
    )
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship("BlogPost", backref="author", lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username {self.username}"