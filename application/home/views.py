from flask import render_template
from . import bp_home


@bp_home.route('/base_index1')
def base_index1():
    return render_template('base_index1.html')


@bp_home.route('/home')
def home():
    return render_template('home/home.html')


@bp_home.route('/')
@bp_home.route('/index')
def index():
    return render_template('home/index.html')
