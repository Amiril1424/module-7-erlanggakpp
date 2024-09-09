from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, Numeric, ForeignKey
from sqlalchemy.sql import func


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(100), nullable=False)
    price = db.Column(Integer)
    description = db.Column(String(255))
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())

    # Relationship List
    reviews = relationship("ProductReview", cascade="all,delete-orphan")
