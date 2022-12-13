#!/usr/bin/python3
"""Place objects that handles all default RESTFul API actions"""

from flask import Flask, Blueprint
from flask import abort, make_response
from flask import jsonify, request
from models import storage, city, place
from api.v1.views import app_views


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def places():
    """ defines places """

    places = []
    the_places = storage.all('Place').values()
    for place in the_places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/cities/<string:city_id>/places', methods=['GET'], strict_slashes=False)
def places_city_id(city_id):
    """Retrieve an object into a valid JSON"""

    places = []
    the_city = storage.get('City', city_id)
    if the_city is None:
        abort(404)
    for place in the_city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'], strict_slashes=False)
def place_id(place_id):
    """Returns an object by id into a valid JSON"""

    the_place = storage.get('Place', place_id)
    if the_place is None:
        abort(404)
    return jsonify(the_place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'], strict_slashes=False)
def place_id_delete(place_id):
    """Deletes a Place object"""

    the_place = storage.get('Place', place_id)
    if the_place is None:
        abort(404)
    the_place.delete()
    storage.save()
    return jsonify({})


@app_views.route('cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place object"""

    our_city = storage.get('City', city_id)
    if our_city is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    my_user = storage.get('User', request.json.get('user_id', ""))
    if my_user is None:
        abort(404)
    rq = request.get_json(silent=True)
    rq['city_id'] = city_id
    my_place = place.Place(**rq)
    storage.new(my_place)
    my_place.save()
    return make_response(jsonify(my_place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""

    my_place = storage.get('Place', place_id)
    if my_place is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for rq in request.get_json(silent=True):
        if rq not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(my_place, rq, request.json[rq])
    my_place.save()
    return jsonify(my_place.to_dict())


if __name__ == "__main__":
    pass
