from flask import Blueprint

bp_search = Blueprint('bp_search', __name__)

from . import views