from flask import Blueprint, request, jsonify
from requests import get
from laguinho.extensions import mongo
from laguinho.routes.metadata import metadata_db
from laguinho.routes.microservices import microservices_metadata

datasets = Blueprint('datasets', __name__)


@datasets.route('/datasets/<owner>/<repo>',
                methods=['GET'],
                strict_slashes=False)
def retrieve_dataset(owner, repo):
    name = owner + '/' + repo
    metadata = metadata_db.find_one({'name': name})
    microservice = microservices_metadata.find_one(
        {'name': metadata['source']})
    print(metadata)
    print(microservice)
    if not metadata or not microservice:
        return '', 404

    response = get(microservice['baseURL'] + '/datasets/' + name,
                   params={'path': metadata['path']})

    return response.json(), 201
