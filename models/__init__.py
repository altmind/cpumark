from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PerfRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    kind = db.Column(db.String(20), index=True)
    other_names = db.Column(db.Text())
    price = db.Column(db.Numeric())
    cpu_mark = db.Column(db.Float())
    cpu_value = db.Column(db.Float())
    cpu_st_mark = db.Column(db.Float())
    cpu_st_value = db.Column(db.Float())
    cpu_tdp = db.Column(db.Float())
    cpu_power_perf = db.Column(db.Float())
    test_date = db.Column(db.Float())
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.current_timestamp())

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return '<PerfRecord %r>' % self.id
