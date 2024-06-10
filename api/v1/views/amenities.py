#!/usr/bin/python3
"""
route for handling Amenity objects and operations
"""
from flask import jsonify, request
from werkzeug.exceptions import NotFound, BadRequest

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities(amenity_id=None):
    """
    Retrieves the list of all Amenity objects or a specific one by ID.

    Parameters
    ----------
    amenity_id : str, optional
        The ID of the Amenity to retrieve. If None, retrieves all Amenities.

    Returns
    -------
    dict
        A dictionary representation of the Amenity(s),
        or an empty dictionary if not found.
    """
    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            return jsonify(amenity.to_dict())
        raise NotFound()

    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes a Amenity object.

    Parameters
    ----------
    amenity_id : str
        The ID of the Amenity to delete.

    Returns
    -------
    dict
        An empty dictionary with status code 200 if successful,
        otherwise raises NotFound.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates a new Amenity.

    Returns
    -------
    dict
        A dictionary representation of the new Amenity with status code 201.
    """
    data = request.get_json()
    if not isinstance(data, dict):
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates a Amenity object.

    Parameters
    ----------
    amenity_id : str
        The ID of the Amenity to update.

    Returns
    -------
    dict
        A dictionary representation of the updated
        Amenity with status code 200.
    """
    ignore_keys = ['id', 'created_at', 'updated_at']
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        data = request.get_json()
        if not isinstance(data, dict):
            raise BadRequest(description='Not a JSON')
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    raise NotFound()
