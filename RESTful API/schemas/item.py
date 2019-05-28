from ma import ma
from models.item import ItemModel
from models.store import StoreModel


class ItemSchema(ma.ModelSchema):
    class Meta:
        model = ItemModel
        # not dump (return as json)
        load_only = ("store",)
        dump_only = ("id",)
        # include foreign key (store id)
        include_fk = True
