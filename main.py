from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions
from flask_sqlalchemy import SQLAlchemy
import os

script_cwd = os.path.dirname(os.path.realpath(__file__))

app = FlaskAPI(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/passmark.db' % script_cwd
db = SQLAlchemy(app)

class PerfRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    kind = db.Column(db.String(20), index=True)
    other_names = db.Column(db.Text())
    price = db.Column(db.Decimal())
    cpu_mark = db.Column(db.Float())
    cpu_value = db.Column(db.Float())
    cpu_st_mark = db.Column(db.Float())
    cpu_st_value = db.Column(db.Float())
    cpu_tdp = db.Column(db.Float())
    cpu_power_perf = db.Column(db.Float())
    test_date = db.Column(db.Float())
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.current_timestamp())

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/api/v1/cpu', methods=['GET'])
def hello_world():
    cpu_data = PassMarkParser()
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
