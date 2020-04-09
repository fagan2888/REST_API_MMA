from flask import Flask, make_response, jsonify, abort, g
from flask_restful import Resource, Api  # type: ignore
from flask_httpauth import HTTPBasicAuth  # type: ignore

import utils
from models import db, bcrypt
from models.users import User
from models.favorite_fighters import FavoriteFighter
from config import app_config

app = Flask(__name__)
app.config.from_object(app_config['testing'])
api = Api(app)
auth = HTTPBasicAuth()
bcrypt.init_app(app)
db.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'URL is not found'}), 404)


@auth.verify_password
def verify(username, password):
    user = User.query.filter_by(email=username).first()

    if not user:
        return False

    g.user = user  # g is a Flask object for view functions to access

    return bcrypt.check_password_hash(user.password, password)


class Home(Resource):
    def get(self):
        return 'www.bestfightodds.com API'


class EventList(Resource):
    def get(self):
        return utils.get_event_list()


class OddsMakersList(Resource):
    def get(self):
        return utils.get_odds_makers_list()


class NumEvents(Resource):
    def get(self):
        return utils.get_num_events()


class FighterList(Resource):
    def get(self, event_id: int):
        return utils.get_fighter_list(event_id)


class FighterOdds(Resource):
    def get(self, fighter_name: str):
        return utils.get_fighter_odds(fighter_name)


class GetFavoriteFighters(Resource):
    @auth.login_required
    def get(self):
        favorite_fighters = []

        fighters = FavoriteFighter.query.filter_by(user_id=g.user.id)
        for fighter in fighters:
            favorite_fighters.append(fighter.fighter_name.lower())

        return utils.get_favorite_fighters(favorite_fighters)


class AddFavoriteFighter(Resource):
    @auth.login_required
    def post(self, fighter_name: str):
        user_id = g.user.id
        user_email = g.user.email

        if FavoriteFighter.get_fighter(user_id, fighter_name.lower()) is not None:
            abort(400, f'{fighter_name} already set for {user_email}.')

        favorite_fighter = FavoriteFighter(user_id, fighter_name.lower())
        favorite_fighter.save()

        return f'Success, {fighter_name} added for {user_email}.'


class DeleteFavoriteFighter(Resource):
    @auth.login_required
    def post(self, fighter_name: str):
        user_id = g.user.id
        user_email = g.user.email
        favorite_fighter = FavoriteFighter.get_fighter(user_id, fighter_name.lower())

        if favorite_fighter:
            favorite_fighter.delete()
            return f'Success, {fighter_name} deleted for {user_email}.'
        else:
            return f'{fighter_name} is not a favorite fighter for {user_email}.'


class AddUser(Resource):
    def post(self, username: str, password: str):
        if (not username) or (not password):
            abort(400, 'Missing username and/or password')
        if User.get_user_by_email(username) is not None:
            abort(400, f'{username} already exists.')

        user = User(username, password)  # password is hashed
        user.save()

        return f'Success, {username} added.'


class DeleteUser(Resource):
    @auth.login_required
    def post(self, username: str):
        if not username:
            abort(400, 'Missing username.')

        user = User.get_user_by_email(username)
        if user is None:
            abort(400, f'{username} does not exists.')
        elif user.email != g.user.email:
            abort(400, f'You may only delete your own account. Sign in as {user.email} to delete.')

        user.delete()

        return f'Success, {username} deleted.'


api.add_resource(Home, '/')
api.add_resource(EventList, '/event_list')
api.add_resource(OddsMakersList, '/odds_makers_list')
api.add_resource(NumEvents, '/num_events')
api.add_resource(FighterList, '/fighter_list/<int:event_id>')
api.add_resource(FighterOdds, '/odds/<fighter_name>')
api.add_resource(GetFavoriteFighters, '/fav_fighters')
api.add_resource(AddFavoriteFighter, '/add_fav_fighter/<fighter_name>')
api.add_resource(DeleteFavoriteFighter, '/delete_fav_fighter/<fighter_name>')
api.add_resource(AddUser, '/add_user/<username>/<password>')
api.add_resource(DeleteUser, '/delete_user/<username>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
