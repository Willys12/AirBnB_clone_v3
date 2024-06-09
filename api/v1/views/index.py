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
    return jsonify({"status": "Ok"})

@app_views.route('/stat', methods=['GET'], strict_slashes=False)
def stat():
    """
    Stats route.
    This route retrieves the count of each object type
    and returns a JSON response.
    """
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    response = jsonify(stats)
    response.status_code = 200

    return response
