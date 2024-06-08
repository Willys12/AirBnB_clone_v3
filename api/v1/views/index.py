#!/usr/bin/python3
"""
This module sets up the status route for the API,
returning a JSON response indicating the service status.
"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def status():
    """
    This route returns a JSON response indicating that
    the API service is running.
    Example response: {"status": "OK"}
    """
    return jsonify({"status": "Ok"})
