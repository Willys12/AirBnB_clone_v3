#!/usr/bin/python3
"""
Flask web application setup.
This module initializes the Flask app, registers blueprints,
and sets up teardown methods and server configuration.
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os

# Initialize Flask application
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    Teardown method to close the storage session.
    This method is called after each request to ensure
    that the storage session is properly closed.
    """
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
