#!/usr/bin/python3
"""
This module initializes the app_views blueprint and
imports all routes from the index module
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import all routes from index module
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
