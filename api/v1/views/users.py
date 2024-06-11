#!/usr/bin/python3
"""
This module initializes the app_views blueprint
and imports all routes from the index module.
"""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User
from werkzeug.exceptions import NotFound, BadRequest


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """
    Retrieves the list of all User objects.

    Returns:
    --------
        A list of all User objects.
    """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object by ID.

    Params:
    -------
        user_id: User id.

    Returns:
    --------
        The User object with the specified id.
        Raises a NotFound exception if the object does not exist.
    """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object.

    Params:
    -------
        user_id: User id.

    Returns:
    --------
        An empty dictionary with status code 200 if the deletion
        was successful.
        Raises a NotFound exception if the object does not exist.
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a User object.

    Returns:
    --------
        The created User object with status code 201.
        Raises a BadRequest exception if the request
        body is not a valid JSON or if it does not contain
        the required keys "email" and "password".
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """
    Updates a User object.

    Params:
    -------
        user_id: User id.

    Returns:
    --------
        The updated User object with status code 200.
        Raises a NotFound exception if the object does not exist.
        Raises a BadRequest exception if the
        request body is not a valid JSON.
    """
    user = storage.get(User, user_id)
    if user:
        if not request.is_json:
            abort(400, description="Not a JSON")
        data = request.get_json()
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
