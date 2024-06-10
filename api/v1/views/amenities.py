#!/usr/bin/python3
""""
Create a new view for Amenity objects that handles
all default RESTFul API actions
"""
from flask import jsonify, request
from werkzeug.exceptions import NotFound, BadRequest
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities(amenity_id=None):
    """Retrieves the list of all Amenity objects or specific one by ID

    Params:
    -------
        amenity_id: str, optional
            Amenity object ID

    Returns:
    --------
        list of Amenity objects in JSON format
    """
    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            return jsonify(amenity.to_dict())
        raise NotFound()
    amenities = storage.all(Amenity).values()
    amenities = list(filter(lambda x: x.to_dict(), amenities))
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object by ID

    Params:
    -------
        amenity_id: str
            Amenity object ID

    Returns:
    --------
        empty dictionary with status code 200
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new Amenity object

    Returns:
    --------
        new Amenity object in JSON format with status code 201
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
    Updates amenity object.

    Params:
    -------
        amenity_id: str
            Amenity object ID

    Returns:
    --------
        updated Amenity object in JSON format with status code 200
    """
    ignore_keys = ('id', 'created_at', 'updated_at')
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
