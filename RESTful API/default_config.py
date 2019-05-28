# use in development env
import os

# Enabling debug model in dev
DEBUG = True
# Connect db
SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"

# Not track the chang of object to save memory
SQLALCHEMY_TRACK_MODIFICATIONS = False

# To use the error handler written in this program, rather than the default value of flask
# When error happens, and there is no catch for it, the error will propagate to
# the app level. ValidationError will be caught by @app.errorhandler
PROPAGATE_EXCEPTIONS = True

# root folder of all the upload files
UPLOADED_IMAGES_DEST = os.path.join("static", "images")  # manage root folder

# Secret key of JWT
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]

# enable blacklist feature
JWT_BLACKLIST_ENABLED = True

# allow blacklisting for access and refresh tokens
JWT_BLACKLIST_TOKEN_CHECKS = [
    "access",
    "refresh",
]
