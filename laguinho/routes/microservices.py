from flask import Blueprint, request, jsonify
from laguinho.models.microservice import microservice_metadata
from marshmallow import ValidationError, EXCLUDE
from laguinho.extensions import mongo

microservices = Blueprint('microservices', __name__)
microservices_metadata = mongo.db.microservices


def microservice_exists(microservice):
    return microservices_metadata.find_one({'ip': microservice['ip']})


@microservices.route('/microservices', methods=['POST'], strict_slashes=False)
def publish():
    result = microservices_metadata.load(request.json, unknown=EXCLUDE)
    if microservice_exists(result):
        return jsonify('Microservice already exists'), 409
    microservices_metadata.insert_one(result)
    return jsonify(result), 201
