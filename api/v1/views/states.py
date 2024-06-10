#!/usr/bin/python3
"""
State objects view.
This module handles all default RESTFul API actions for State objects.
"""

from flask import jsonify, request, abort
# from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all state objects.
    Returns:
        A JSON response containing the list of all state objects.
    """
    states = [state.to_dict() for state in State.all()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object by its ID.
    Args:
        state_id (str): The ID of the State object.
    Returns:
        A JSON response containing the State object.
    """
    state = State.get(state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object by its ID.
    Args:
        state_id (str): The ID of the State object.
    Returns:
        An empty JSON response with status code 200 if successful.
    """
    state = State.get(state_id)
    if state is None:
        abort(404)
    state.delete()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a new State object.
    Returns:
        A JSON response containing the newly created State object.
    """
    if not request.json:
        abort(400, description='Not a JSON')

    data = request.get_json()
    if 'name' not in request.json:
        abort(400, description='Missing name')

    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object by its ID.
    Args:
        state_id (str): The ID of the State object.
    Returns:
        A JSON response containing the updated State object.
    """
    state = state.get(state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, description='Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
