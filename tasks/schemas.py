from marshmallow import Schema, fields

class TaskSchema(Schema):
    _id = fields.Str(required=True)
    title = fields.Str()
    description = fields.Str()
    done = fields.Bool()
