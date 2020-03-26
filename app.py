from flask import Flask, make_response, jsonify
from flask_restful import Resource, Api  # type: ignore
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from passlib.hash import sha256_crypt
import os

import utils
from models import db, bcrypt
from models.users import UserModel

def create_app(app):
    api = Api(app)
    auth = HTTPBasicAuth()

    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    bcrypt.init_app(app)
    db.init_app(app)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    @auth.verify_password
    def verify(username, password):
        user = UserModel.query.filter_by(email = username).first()

        if not user:
            return False

        return bcrypt.check_password_hash(user.password, password)

    class Home(Resource):
        @auth.login_required
        def get(self):
            return 'www.bestfightodds.com API'


    class EventList(Resource):
        @auth.login_required
        def get(self):
            return utils.get_event_list()


    class OddsMakersList(Resource):
        @auth.login_required
        def get(self):
            return utils.get_odds_makers_list()


    class NumEvents(Resource):
        @auth.login_required
        def get(self):
            return utils.get_num_events()


    class FighterList(Resource):
        @auth.login_required
        def get(self, event_id):
            return utils.get_fighter_list(event_id)


    class FighterOdds(Resource):
        @auth.login_required
        def get(self, fighter_name):
            return utils.get_fighter_odds(fighter_name)


    api.add_resource(Home, '/')
    api.add_resource(EventList, '/event_list')
    api.add_resource(OddsMakersList, '/odds_makers_list')
    api.add_resource(NumEvents, '/num_events')
    api.add_resource(FighterList, '/fighter_list/<event_id>')
    api.add_resource(FighterOdds, '/odds/<fighter_name>')

if __name__ == '__main__':
    app = Flask(__name__)
    create_app(app)
    app.run(debug=True)
