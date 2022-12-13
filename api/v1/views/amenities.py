#!/usr/bin/python3
"""Contains amenities module"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id=None):
    """ list of all Amenity objects"""

    if amenity_id is None:
        amenities = [amenity.to_dict() for amenity
                     in storage.all("Amenity").values()]
        return jsonify(amenities)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id=None):
    """Deletes a Amenity object"""

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates a Amenity object"""

    try:
        rq = request.get_json()
    except:
        rq = None
    if rq is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in rq:
        return make_response(jsonify({'error': "Missing name"}), 400)
    amenity = Amenity(**rq)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id=None):
    """Updates a Amenity object"""

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    try:
        rq = request.get_json()
    except:
        rq = None
    if rq is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for k, val in rq.items():
        if k not in ('id', 'created_at', 'updates_at'):
            setattr(amenity, k, val)
    amenity.save()
    return jsonify(amenity.to_dict())
