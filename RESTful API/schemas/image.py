from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage


# This marshmallow field is just used to deserialize the data
class FileStorageField(fields.Field):
    default_error_messages = {
        "invalid": "Not a valid image."
    }

    # will run when load() is called
    def _deserialize(self, value, attr, data) -> FileStorage:
        if value is None:
            return None

        if not isinstance(value, FileStorage):
            self.fail("invalid")  # fail is a method defined in Field. It will raise Validation Error

        return value


# The schema is just used to validate the image
class ImageSchema(Schema):
    image = FileStorageField(required=True)
