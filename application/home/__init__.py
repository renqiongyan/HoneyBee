from flask import Blueprint

bp_home = Blueprint('bp_home', __name__)

from . import views