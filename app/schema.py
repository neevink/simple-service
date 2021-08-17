from marshmallow import Schema
from marshmallow.fields import (
    Int, Str,
)
from marshmallow.validate import Length


# Сервис по продаже симпл-димплов

class CustomerSchema(Schema):
    """Заказчик"""
    name = Str(required=True, validate=Length(1, 32))
    address = Str(required=True, validate=Length(1, 64))

