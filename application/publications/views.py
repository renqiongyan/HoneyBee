from flask import render_template
from . import bp_publications


@bp_publications.route('/')
@bp_publications.route('/publications')
def publications():
    return render_template('publications/publications.html')
