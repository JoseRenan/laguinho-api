from marshmallow import Schema, fields, validate
from .error_messages import get_required_error


class MicroserviceMetadataSchema(Schema):
    name = fields.Str(required=True, error_messages=get_required_error('name'))
    baseURL = fields.Str(required=True,
                         error_messages=get_required_error('baseURL'))


microservice_metadata = MicroserviceMetadataSchema()
