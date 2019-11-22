from flask import Blueprint, request, jsonify
from laguinho.models.metadata import dataset_metadata
from marshmallow import ValidationError, EXCLUDE
from laguinho.extensions import mongo

metadata = Blueprint('metadata', __name__)
metadata_db = mongo.db.metadata


def dataset_exists(dataset):
    return metadata_db.find_one({
        '$or': [{
            'name': dataset['name']
        }, {
            'url': dataset['url'],
            'path': dataset['path']
        }]
    })


@metadata.route("/metadata", methods=['POST'], strict_slashes=False)
def publish():
    result = dataset_metadata.load(request.json, unknown=EXCLUDE)
    if dataset_exists(result):
        return jsonify('Dataset already exists'), 409
    metadata_db.insert_one(result)
    del result['_id']
    return jsonify(result), 201


@metadata.route("/metadata", methods=['GET'], strict_slashes=False)
def get_datasets_metadata():
    dsets = list(metadata_db.find())
    for ds in dsets:
        del ds['_id']

    return jsonify(dsets)


@metadata.route("/metadata/<name>", methods=['GET'], strict_slashes=False)
def get_datasets_by_name(name):
    search_result = metadata_db.find_one_or_404({'name': name})
    del search_result['_id']
    return jsonify(search_result), 200
