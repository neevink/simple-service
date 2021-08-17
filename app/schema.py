from marshmallow import Schema
from marshmallow.fields import (
    Int, Str,
)
from marshmallow.validate import Length


# Сервис по установке кулеров для воды и услуг по доставке воды в эти кулеры

class CustomerSchema(Schema):
    """Заказчик"""
    name = Str(required=True, validate=Length(1, 32))
    address = Str(required=True, validate=Length(1, 64))

