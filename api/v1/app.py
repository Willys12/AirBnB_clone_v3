#!/usr/bin/python3
"""
Flask web application setup.
This module initializes the Flask app, registers blueprints,
and sets up teardown methods and server configuration.
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os


# Initialize Flask application
app = Flask(__name__)
"""Flask application instance"""
a_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
a_port = int(os.getenv('HBNB_API_PORT', '5000'))
CORS(app, resources={'/*': {'origins': a_host}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    Teardown method to close the storage session.
    This method is called after each request to ensure
    that the storage session is properly closed.
    """
    storage.close()


@app.errorhandler(404)
def resource_not_found(e):
    """404 error handler"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    a_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    a_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=a_host, port=a_port, threaded=True)
