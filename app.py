import os
from flask import Flask
from dotenv import load_dotenv
from connector.mysql_connector import connection
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager
from db import db
from flask_migrate import Migrate

from models.users import User
from models.products import Product
from models.product_reviews import ProductReview

from controllers.users import users_blueprints
from controllers.products import products_blueprints
from controllers.product_reviews import product_reviews_blueprints

load_dotenv()

app = Flask(__name__)


username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_DATABASE")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://{username}:{password}@{host}/{database}"
app.config["SESSION_COOKIE_NAME"] = "session"
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = 600

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(users_blueprints)
app.register_blueprint(products_blueprints)
app.register_blueprint(product_reviews_blueprints)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    Session = sessionmaker(bind=connection)
    s = Session()
    try:
        user = s.query(User).get(int(user_id))
        return user
    except Exception as e:
        print(f"Error loading user: {e}")
        return None
    finally:
        s.close()


@app.route("/")
def index():

    return "Hello World!"
