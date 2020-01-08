from flask import render_template
from . import bp_download


@bp_download.route('/')
@bp_download.route('/download')
def download():
    return render_template('download/download.html')
