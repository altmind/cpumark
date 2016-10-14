# coding:utf-8
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from pass_mark_parser import PassMarkParser
import os
from models import *

if __name__ == '__main__':
    script_cwd = os.path.dirname(__file__)

    app = FlaskAPI(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/passmark.db' % script_cwd
    db.init_app(app)
    with app.test_request_context():
        db.engine.text_factory = str
        db.create_all()


    @app.route('/api/v1/cpu', methods=['GET'])
    def get_all():
        return PerfRecord.query.all()


    @app.route('/api/v1/cpu/update', methods=['POST'])
    def update():
        rows = PassMarkParser().fetch_and_parse()
        for row in rows:
            entry = PerfRecord(**row)
            print repr(entry)
            existing_entry = PerfRecord.query.get(row['id'])
            if (existing_entry is not None):
                db.session.query(PerfRecord).filter(PerfRecord.id == row['id']).update(entry.__dict__)
            else:
                db.session.add(entry)
        db.session.commit()
        return rows


    app.run()
