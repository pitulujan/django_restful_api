from marshmallow import Schema, fields, post_load
from .models import User

class UserSchema(Schema):
    _id = fields.Str(required=True)
    username = fields.Str()
    password = fields.Str()
    admin = fields.Bool()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
