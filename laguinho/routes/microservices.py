from flask import Blueprint, request, jsonify
from laguinho.models.microservice import microservice_metadata
from marshmallow import ValidationError, EXCLUDE
from laguinho.extensions import mongo

microservices = Blueprint('microservices', __name__)
microservices_metadata = mongo.db.microservices


def microservice_exists(microservice):
    return microservices_metadata.find_one({'name': microservice['name']})


@microservices.route('/microservices', methods=['POST'], strict_slashes=False)
def publish():
    result = microservice_metadata.load(request.json, unknown=EXCLUDE)
    if microservice_exists(result):
        return jsonify('Microservice already exists'), 409
    microservices_metadata.insert_one(result.copy())
    return jsonify(result), 201


@microservices.route('/microservices/<name>',
                     methods=['DELETE'],
                     strict_slashes=False)
def remove_microservice(name):
    if microservice_exists({'name': name}):
        microservices_metadata.delete_one({'name': name})
        return '', 204
    return '', 404
