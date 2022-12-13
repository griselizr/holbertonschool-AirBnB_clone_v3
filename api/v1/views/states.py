
#!/usr/bin/python3
"""creates objects that handles all default RESTFul API actions"""

from flask import Flask, Blueprint
from flask import abort, make_response
from flask import jsonify, request
from models import storage, state
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """Retrieves the list of all State"""
    list_states = []
    states = storage.all('State').values()
    for state in states:
        states.append(list_states.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    """Retrieve an object into a valid JSON"""

    the_id = storage.get('State', state_id)
    if the_id is None:
        abort(404)
    return jsonify(the_id.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'], strict_slashes=False)
def state_id_delete(state_id):
    """Deletes a State object"""

    my_state = storage.get('State', state_id)
    if my_state is None:
        abort(404)
    my_state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """Returns the new State with the status code 201"""

    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    the_state = state.State(name=request.json.get('name', ""))
    storage.new(the_state)
    the_state.save()
    return make_response(jsonify(the_state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Returns the State object with the status code 200"""

    in_state = storage.get('State', state_id)
    if in_state is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for rq in request.json:
        if rq not in ['id', 'created_at', 'updated_at']:
            setattr(in_state, rq, request.json[rq])
    in_state.save()
    return jsonify(in_state.to_dict())


if __name__ == "__main__":
    pass
