#!/usr/bin/python3
"""handles all default RestFul API action"""

from flask import jsonify, request, abort, make_response
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def all_cities(state_id):
    """return the all City objects"""

    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    toda_ciudad = []
    cities = storage.all(City).values()
    for city in cities:
        if city.state_id == state_id:
            toda_ciudad.append(city.to_dict())
    return jsonify(toda_ciudad)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_id(city_id):
    """return City object by id """

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city = city.to_dict()
    return jsonify(city)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """delete City"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    response = make_response(jsonify({}), 200)
    return response


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """create a new City"""

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    json_f = request.get_json()
    if not json_f:
        return make_response("Not a JSON", 400)
    if "name" not in json_f:
        return make_response("Missing name", 400)
    json_f["state_id"] = state_id
    new_city = City(**json_f)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """update a City object by id"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    json_f = request.get_json()
    if not json_f:
        return make_response("Not a JSON", 400)
    for k, value in json_f.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if k not in ignore_keys:
            setattr(city, k, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
