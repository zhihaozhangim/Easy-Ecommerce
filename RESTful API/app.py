# Import Flask
from flask import Flask, jsonify
from flask_restful import Api

# Used for authentication (login, log out)
from flask_jwt_extended import JWTManager

# must be loaded before oauth
from dotenv import load_dotenv

# Allow us to use .env before app starts
load_dotenv(".env", verbose=True)
# SQLAlchemy

from db import db

# Import flask_marshmallow for converting complex objects to and from simple Python data types
from ma import ma

# Black list of jwt
from blacklist import BLACKLIST

# Import resources
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout

# Import Models
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.confirmation import Confirmation, ConfirmationByUser

# Used for app level error handler
from marshmallow import ValidationError
from flask_uploads import configure_uploads, patch_request_class
from resources.image import ImageUpload, Image, AvatarUpload, Avatar
from libs.image_helper import IMAGE_SET

# Used to get .env
import os

from oa import oauth
from resources.github_login import GithubLogin, GithubAuthorize

app = Flask(__name__)


# load default configs from default_config.py
app.config.from_object("default_config")

app.config.from_envvar(
    "APPLICATION_SETTINGS"
)  # override with config.py (APPLICATION_SETTINGS points to config.py)

patch_request_class(app, 10 * 1024 * 1024)  # restrict max upload image size to 10MB
configure_uploads(app, IMAGE_SET)   # Link IMAGE_SET with app

# Use Flask RESTful
api = Api(app)

# Create the db before the first request
@app.before_first_request
def create_tables():
    db.create_all()


# Adding app level error handler, can be seen as a catch when error of given type happens
@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt = JWTManager(app) # Use flask_jwt_extended

# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
# Used for log out
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return (
        decrypted_token["jti"] in BLACKLIST
    )  # Here we blacklist particular JWTs that have been created in the past.


# Relate the resource to the end point
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
# html page
api.add_resource(Confirmation, "/user_confirm/<string:confirmation_id>")
# get user info or resend email
api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")
api.add_resource(ImageUpload, "/upload/image")
api.add_resource(Image, "/image/<string:filename>")
api.add_resource(AvatarUpload, "/upload/avatar")
api.add_resource(Avatar, "/avatar/<int:user_id>")
api.add_resource(GithubLogin, "/login/github")
api.add_resource(GithubAuthorize, "/login/github/authorized")


# Prevent import loop, this file is the entry point of the program
if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    oauth.init_app(app)
    app.run(port=5000, debug=True)
