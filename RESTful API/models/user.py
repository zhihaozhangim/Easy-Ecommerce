from requests import Response
from flask import request, url_for
from db import db
from libs.mailgun import Mailgun
from models.confirmation import ConfirmationModel


# Make this model a SQLAlchemy Model
class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    # Cannot be null, not need __init__ here, because the __init__
    # will be created automatically and accept the two nullable args
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)

    # lazy=dynamic means confirmation will not be retrieved from db when create a new user model
    # Instead, will retrieve it only when access it. We can create a user model without confirmation
    # If we create one afterwards, we can still access it from the user

    # delete-orphan means if the user is deleted, all confirmations related to it will be deleted
    confirmation = db.relationship(
        "ConfirmationModel", lazy="dynamic", cascade="all, delete-orphan"
    )

    # If the user have multiple confirmations, get the most recent one.
    @property
    def most_recent_confirmation(self) -> "ConfirmationModel":
        # ordered by expiration time (in descending order)
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    # Send request to mail gun
    def send_confirmation_email(self) -> Response:
        # string[:-1] means copying from start (inclusive) to the last index (exclusive), a more detailed link below:
        # from `http://127.0.0.1:5000/` to `http://127.0.0.1:5000`, since the url_for() would also contain a `/`
        # https://stackoverflow.com/questions/509211/understanding-pythons-slice-notation
        # userconfirm -> UserConfirm -> user_confirm/1
        subject = "Registration Confirmation"
        link = request.url_root[:-1] + url_for("confirmation", confirmation_id=self.most_recent_confirmation.id)
        text = f"Please click the link to confirm your registration: {link}"
        html = f"<html>Please click the link to confirm your registration: <a href={link}>link</a></html>"
        return Mailgun.send_email([self.email], subject, text, html)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
