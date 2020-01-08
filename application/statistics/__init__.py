from flask import Blueprint

bp_statistics = Blueprint('bp_statistics', __name__)

from . import views