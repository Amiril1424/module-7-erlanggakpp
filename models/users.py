from db import db
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from flask_login import UserMixin
import bcrypt


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    email = db.Column(String(100), nullable=False)
    name = db.Column(String(100), nullable=False)
    password = db.Column(String(100), nullable=False)
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    role = db.Column(String(100))

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
