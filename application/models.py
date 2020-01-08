from wtforms import StringField

from .extensions import flask_db


class Gene_loc():
    species = StringField()
    gene = StringField()
    chromosome = StringField
    start = StringField
    end = StringField
    direction = StringField(null=False, choices=(('+', '正向'), ('-', '反向'), ('.', '未知方向')))

    class Meta:
        database = flask_db.database


class Gene_seq():
    species = StringField()
    gene = StringField()
    function = StringField()
    seq = StringField()

    class Meta:
        database = flask_db.database


class Gene_struc():
    species = StringField()
    gene = StringField()
    struID = StringField()
    struName = StringField()

    class Meta:
        database = flask_db.database
