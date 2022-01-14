from marshmallow import Schema
from marshmallow.fields import (
    Int, Str,
)
from marshmallow.validate import Length


class CustomerSchema(Schema):
    """Заказчик"""
    name = Str(required=True, validate=Length(1, 32))
    address = Str(required=True, validate=Length(1, 64))


class PostCreateSchema(Schema):
    user_id = Int(required=True)
    post_text = Str(required=True, validate=Length(1, 255))
