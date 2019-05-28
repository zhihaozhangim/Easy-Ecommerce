from time import time
from uuid import uuid4

from db import db

CONFIRMATION_EXPIRATION_DELTA = 1800  # 30 minutes


class ConfirmationModel(db.Model):
    __tablename__ = "confirmations"

    id = db.Column(db.String(50), primary_key=True)
    # How long a confirmation will last for until it expires
    expire_at = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # Only after the model is loaded, the user the be populated. Not in DB
    user = db.relationship("UserModel")

    def __init__(self, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        # universally unique identifier version 4 as a string
        self.id = uuid4().hex
        # time gives the current time since 01/01/1970
        self.expire_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA
        self.confirmed = False

    @classmethod
    def find_by_id(cls, _id: str) -> "ConfirmationModel":
        return cls.query.filter_by(id=_id).first()

    @property
    # can be accessed using confirmation.expired which means it doesn't chang anything
    # and confirmation.expired in the class field cannot be called. can only call expired() to access it
    def expired(self) -> bool:
        return time() > self.expire_at

    def force_to_expire(self) -> None:  # forcing current confirmation to expire
        if not self.expired:    # actually call self.expired() method because of property decorator
            self.expire_at = int(time())
            self.save_to_db()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
