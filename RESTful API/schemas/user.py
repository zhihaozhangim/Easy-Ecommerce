from marshmallow import pre_dump

from ma import ma
from models.user import UserModel


class UserSchema(ma.ModelSchema):
    class Meta:
        # Link the schema with user model, and create the fields based on the
        # columns of the user model. If it ok, the load method will return a
        # user model
        model = UserModel
        # only load password, not dump it. Don't return it to front end
        load_only = ("password",)
        # Do not load the id, because the front end won't pass it to the back end
        dump_only = ("id", "activated")

        # Will run before the dump method to turn an obj into json
        # In this case, we just get the most recent confirmation
        @pre_dump
        def _pre_dump(self, user: UserModel):
            user.confirmation = [user.most_recent_confirmation]
            return user
