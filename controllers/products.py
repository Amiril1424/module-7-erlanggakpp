from flask import Blueprint, request
from connector.mysql_connector import connection
from models.products import Product

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from flask_login import login_required, current_user
from decorator.role_checker import role_required

products_blueprints = Blueprint("products_blueprints", __name__)


@products_blueprints.route("/product", methods=["GET"])
@login_required
def show():
    Session = sessionmaker(bind=connection)
    s = Session()

    try:
        product_query = s.query(Product)

        result = product_query.all()

        products = []
        for product in result:
            products.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "description": product.description,
                }
            )

    except Exception as e:
        print(e)
        return {"message": "An error occurred while fetching products."}, 500

    finally:
        s.close()

    return {
        "message": f"Product list successfully retrieved by {current_user.name}.",
        "products": products,
    }, 200


@products_blueprints.route("/product", methods=["POST"])
# @role_required("admin")
@login_required
def add():
    Session = sessionmaker(bind=connection)
    s = Session()

    try:
        s.begin()

        new_product = Product(
            name=request.form["name"],
            price=request.form["price"],
            description=request.form["description"],
        )

        s.add(new_product)
        s.commit()

        result = {
            "id": new_product.id,
            "name": new_product.name,
            "price": new_product.price,
            "description": new_product.description,
            "created_at": new_product.created_at,
        }

    except Exception as e:
        s.rollback()
        print(e)
        return {"message": "Failed to insert product."}, 500

    finally:
        s.close()

    return {
        "message": "Product added successfully to the catalog.",
        "product": result,
    }, 200


@products_blueprints.route("/product/<id>", methods=["GET"])
@login_required
def show_by_id(id):
    Session = sessionmaker(bind=connection)
    s = Session()
    try:
        product_query = s.query(Product).filter(Product.id == id).first()
        if product_query is None:
            return {"message": "Product doesn't exist"}, 404

        result = {
            "id": product_query.id,
            "name": product_query.name,
            "price": product_query.price,
            "description": product_query.description,
        }

    except Exception as e:
        print(e)
        return {"message": "An error occurred while fetching product."}, 500

    finally:
        s.close()

    return {
        "message": f"Product successfully retrieved by {current_user.name}.",
        "products": result,
    }, 200


@products_blueprints.route("/product/<id>", methods=["PUT"])
@login_required
@role_required("Admin")
def update(id):
    Session = sessionmaker(bind=connection)
    s = Session()

    try:
        s.begin()

        product = s.query(Product).filter(Product.id == id).first()

        if product is None:
            return {"message": "The product you're trying to update doesn't exist."}, 404

        product.name = request.form["name"]
        product.price = request.form["price"]
        product.description = request.form["description"]

        s.commit()

        result = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description,
        }

    except Exception as e:
        s.rollback()
        print(e)
        return {"message": "An error occurred while trying to update the product."}, 500

    finally:
        s.close()

    return {
        "message": f"Product updated successfully by {current_user.name}.",
        "product": result,
    }, 200


@products_blueprints.route("/product/<id>", methods=["DELETE"])
@login_required
@role_required("Admin")
def delete(id):
    Session = sessionmaker(bind=connection)
    s = Session()

    try:
        s.begin()
        product = s.query(Product).filter(Product.id == id).first()
        if product is None:
            return {"message": "The product you're trying to delete doesn't exist."}, 404

        result = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description,
        }

        s.delete(product)
        s.commit()

    except Exception as e:
        s.rollback()
        print(e)
        return {"message": "An error occurred while trying to delete the product."}, 500

    finally:
        s.close()
    return {
        "message": f"Product deleted successfully by {current_user.name}.",
        "product": result,
    }, 200
