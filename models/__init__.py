# coding:utf-8
from flask_sqlalchemy import SQLAlchemy
from json_encoded_dict import JSONEncodedDict

db = SQLAlchemy()


class PerfRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    kind = db.Column(db.String(20), index=True)
    other_names = db.Column(JSONEncodedDict())
    price = db.Column(db.Numeric())
    cpu_mark = db.Column(db.Float())
    cpu_value = db.Column(db.Float())
    cpu_st_mark = db.Column(db.Float())
    cpu_st_value = db.Column(db.Float())
    tdp = db.Column(db.Float())
    power_perf = db.Column(db.Float())
    test_date = db.Column(db.String(255))
    cpu_socket = db.Column(db.String(255))
    cpu_category = db.Column(db.String(255))
    ext = db.Column(JSONEncodedDict())
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.current_timestamp())

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return '<PerfRecord %s>' % self.name
