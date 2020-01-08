from flask import Blueprint

bp_download = Blueprint('bp_download', __name__)

from . import views