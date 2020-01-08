import json

from flask import render_template, request

from application.utilities import *
from . import bp_search


@bp_search.route('/')

@bp_search.route('/search')
def search():
    return render_template('search/search.html')


@bp_search.route('/search1')
def search1():
    species1 = request.args.get("species1")
    gene = request.args.get("gene")
    print(species1)
    where_condition1 = select_locwhere(species=species1, gene=gene)
    seqs1 = select_all(table_name="gene_loc", where_condition=where_condition1)
    jsonstr1 = json.dumps(seqs1, ensure_ascii=False)
    return jsonstr1


@bp_search.route('/search2')
def search2():
    species2 = request.args.get("species2")
    chromosome = request.args.get("chromosome")
    gstart = request.args.get("gstart")
    gend = request.args.get("gend")
    print(species2)
    where_condition2 = select_locwhere(species=species2, chromosome=chromosome, gstart=gstart, gend=gend)
    seqs2 = select_all(table_name="gene_loc", where_condition=where_condition2)
    print(seqs2)
    jsonstr2 = json.dumps(seqs2, ensure_ascii=False)
    return jsonstr2
