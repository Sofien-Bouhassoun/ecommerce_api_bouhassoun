from datetime import datetime
from passlib.hash import bcrypt
from ..extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="client")  # 'client'|'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, pwd): self.password_hash = bcrypt.hash(pwd)
    def check_password(self, pwd): return bcrypt.verify(pwd, self.password_hash)
