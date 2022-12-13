#!/usr/bin/python3
""" Users"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id=None):
    """Returns all users list"""

    if user_id is None:
        users = [user.to_dict() for user
                 in storage.all("User").values()]
        return jsonify(users)
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id=None):
    """Deletes a User object"""

    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()

    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a User object"""

    try:
        rq = request.get_json()
    except:
        rq = None
    if rq is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in rq:
        return make_response(jsonify({'error': "Missing email"}), 400)
    if 'password' not in rq:
        return make_response(jsonify({'error': "Missing password"}), 400)
    user = User(**rq)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id=None):
    """Updates a User object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    try:
        rq = request.get_json()
    except:
        rq = None
    if rq is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for k, val in rq.items():
        if k not in ('id', 'email', 'created_at', 'updates_at'):
            setattr(user, k, val)
    user.save()
    return jsonify(user.to_dict())


if __name__ == "__main__":
    pass
