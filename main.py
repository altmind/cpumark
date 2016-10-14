from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_sqlalchemy import SQLAlchemy
from pass_mark_parser import PassMarkParser
import os
import sys
from models import *

if __name__ == '__main__':
    script_cwd = os.path.dirname(__file__)

    app = FlaskAPI(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/passmark.db' % script_cwd
    db.init_app(app)
    with app.test_request_context():
        db.create_all()


    @app.route('/api/v1/cpu', methods=['GET'])
    def get_all():
        return PerfRecord.query.all()


    @app.route('/api/v1/cpu/update', methods=['POST'])
    def update():
        parser = PassMarkParser()
        return parser.fetch_and_parse()

    app.run()
