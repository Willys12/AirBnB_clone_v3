#!/usr/bin/python3
"""
This module initializes the app_views blueprint and
imports all routes from the index module
"""
from flask import Blueprint

# Import all routes from index module
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.amenities import *
from api.v1.views.cities import *


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


app_views.register_blueprint(index_routes, url_prefix='/index')
app_views.register_blueprint(states_routes, url_prefix='/states')
app_views.register_blueprint(amenities_routes, url_prefix='/amenities')
app_views.register_blueprint(cities_routes, url_prefix='/cities')
