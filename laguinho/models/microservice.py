from marshmallow import Schema, fields, validate
from .error_messages import get_required_error


class MicroserviceMetadataSchema(Schema):
    name = fields.Str(required=True, error_messages=get_required_error('name'))
    ip = fields.Str(
        required=True,
        error_messages=get_required_error('ip'),
        validate=validate.Regexp('^(?:[0-9]{1,3}\\.){3}[0-9]{1,3}$'))


microservice_metadata = MicroserviceMetadataSchema()
