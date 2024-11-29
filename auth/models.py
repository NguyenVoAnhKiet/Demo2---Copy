from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Tạo model User
class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phonenumber = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
