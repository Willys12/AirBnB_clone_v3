#!/usr/bin/python3
"""
This module sets up the status route for the API,
returning a JSON response indicating the service status.
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    This route returns a JSON response indicating that
    the API service is running.
    Example response: {"status": "OK"}
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stat():
    """
    Stats route.
    This route retrieves the count of each object type
    and returns a JSON response.
    """
    objects = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    response = jsonify(objects)
    response.status_code = 200

    return response
