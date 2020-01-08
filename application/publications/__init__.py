from flask import Blueprint

bp_publications = Blueprint('bp_publications', __name__)

from . import views