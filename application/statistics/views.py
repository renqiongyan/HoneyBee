import json

from flask import render_template, request

from application.utilities import *
from . import bp_statistics


@bp_statistics.route('/')
@bp_statistics.route('/statistics')
def statistics():
    return render_template('statistics/statistics.html')


@bp_statistics.route('/statistic')
def statistic():
    fun = request.args.get("fun")
    print(fun)
    where_condition = "function like '%%%s%%'" % (fun)
    seqs = select_all(table_name="gene_seq", where_condition=where_condition)
    print(seqs[1], len(seqs[0]))
    jsonstr = json.dumps(seqs, ensure_ascii=False)
    return jsonstr


@bp_statistics.route('/test')
def test():
    return render_template('statistics/test.html')

# @bp_statistics.route('/list_seq')
# def list_seq():
#     query = Gene_seq.select().order_by(Gene_seq.gene)
#     pg = PaginatedQuery(query, paginate_by=10, page_var='page', check_bounds=True)
#     page = pg.get_page()
#     page_count = pg.get_page_count()
#     seqs = pg.get_object_list()
#     return render_template('statistics/list_seq.html', seqs=seqs, page=page, page_count=page_count)
