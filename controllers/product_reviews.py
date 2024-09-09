from flask import Blueprint, request
from connector.mysql_connector import connection
from models.product_reviews import ProductReview

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from flask_login import login_required, current_user

product_reviews_blueprints = Blueprint("product_reviews_blueprints", __name__)


@product_reviews_blueprints.route("/product-review", methods=["GET"])
@login_required
def show():
    Session = sessionmaker(bind=connection)
    s = Session()

    try:
        review_query = s.query(ProductReview)

        result = review_query.all()

        reviews = []
        for review in result:
            reviews.append(
                {
                    "id": review.id,
                    "product_id": review.product_id,
                    "email": review.email,
                    "rating": review.rating,
                    "review_content": review.review_content,
                }
            )

    except Exception as e:
        print(e)
        return {"message": "An error occurred while fetching product reviews."}, 500

    finally:
        s.close()

    return {
        "message": f"Product Review list successfully retrieved by {current_user.name}.",
        "products": reviews,
    }, 200


@product_reviews_blueprints.route("/product-review", methods=["POST"])
@login_required
def add():
    Session = sessionmaker(bind=connection)
    s = Session()

    try:
        s.begin()

        new_review = ProductReview(
            product_id=request.form["product_id"],
            email=request.form["email"],
            rating=request.form["rating"],
            review_content=request.form["review_content"],
        )

        s.add(new_review)
        s.commit()

        result = {
            "id": new_review.id,
            "product_id": new_review.product_id,
            "email": new_review.email,
            "rating": new_review.rating,
            "review_content": new_review.review_content,
            "created_at": new_review.created_at,
        }

    except Exception as e:
        s.rollback()
        print(e)
        return {"message": "Failed to insert review."}, 500

    finally:
        s.close()

    return {
        "message": "Review added successfully.",
        "product": result,
    }, 200


@product_reviews_blueprints.route("/product-review/<id>", methods=["GET"])
@login_required
def show_by_id(id):
    Session = sessionmaker(bind=connection)
    s = Session()
    try:
        review_query = s.query(ProductReview).filter(ProductReview.id == id).first()
        if review_query is None:
            return {"message": "Review doesn't exist"}, 404

        result = {
            "id": review_query.id,
            "product_id": review_query.product_id,
            "email": review_query.email,
            "rating": review_query.rating,
            "review_content": review_query.review_content,
        }

    except Exception as e:
        print(e)
        return {"message": "An error occurred while fetching review."}, 500

    finally:
        s.close()

    return {
        "message": f"Review successfully retrieved by {current_user.name}.",
        "reviews": result,
    }, 200


@product_reviews_blueprints.route("/product-review/<id>", methods=["PUT"])
@login_required
def update(id):
    Session = sessionmaker(bind=connection)
    s = Session()

    try:
        s.begin()

        review = s.query(ProductReview).filter(ProductReview.id == id).first()

        if review is None:
            return {"message": "The review you're trying to update doesn't exist."}, 404

        review.product_id = request.form["product_id"]
        review.email = request.form["email"]
        review.rating = request.form["rating"]
        review.review_content = request.form["review_content"]

        s.commit()

        result = {
            "id": review.id,
            "product_id": review.product_id,
            "email": review.email,
            "rating": review.rating,
            "review_content": review.review_content,
            "created_at": review.created_at,
        }

    except Exception as e:
        s.rollback()
        print(e)
        return {"message": "An error occurred while trying to update the review."}, 500

    finally:
        s.close()

    return {
        "message": f"Review updated successfully by {current_user.name}.",
        "review": result,
    }, 200


@product_reviews_blueprints.route("/product-review/<id>", methods=["DELETE"])
@login_required
def delete(id):
    Session = sessionmaker(bind=connection)
    s = Session()

    try:
        s.begin()
        review = s.query(ProductReview).filter(ProductReview.id == id).first()
        if review is None:
            return {"message": "The review you're trying to delete doesn't exist."}, 404

        result = {
            "id": review.id,
            "product_id": review.product_id,
            "email": review.email,
            "rating": review.rating,
            "review_content": review.review_content,
            "created_at": review.created_at,
        }

        s.delete(review)
        s.commit()

    except Exception as e:
        s.rollback()
        print(e)
        return {"message": "An error occurred while trying to delete the review."}, 500

    finally:
        s.close()
    return {
        "message": f"Review deleted successfully by {current_user.name}.",
        "product": result,
    }, 200
