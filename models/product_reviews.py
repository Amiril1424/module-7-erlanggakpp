from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, Numeric, ForeignKey
from sqlalchemy.sql import func


class ProductReview(db.Model):
    __tablename__ = "product_reviews"

    id = db.Column(Integer, primary_key=True)
    product_id = db.Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    email = db.Column(String(30), nullable=False)
    rating = db.Column(Integer)
    review_content = db.Column(String(255))
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
