from typing import List
from db import db


# Make this model a SQLAlchemy Model
class ItemModel(db.Model):
    # Define the name of the table
    __tablename__ = "items"

    # Turn the properties into SQL queries
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    price = db.Column(db.Float(precision=2), nullable=False)

    # Foreign key
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store = db.relationship("StoreModel")

    # Find an item by its name
    @classmethod
    def find_by_name(cls, name: str) -> "ItemModel":
        return cls.query.filter_by(name=name).first()

    # Find all items
    @classmethod
    def find_all(cls) -> List["ItemModel"]:
        return cls.query.all()

    # Save the item to DB
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    # Delete the item from DB
    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
