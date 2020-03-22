from flask import Flask, make_response, jsonify
from flask_restful import Resource, Api
import json

import utils

app = Flask(__name__)
api = Api(app)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

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
	def get(self, event_id):
		return utils.get_fighter_list(event_id)

api.add_resource(Home, '/')
api.add_resource(EventList, '/event_list')
api.add_resource(OddsMakersList, '/odds_makers_list')
api.add_resource(NumEvents, '/num_events')
api.add_resource(FighterList, '/fighter_list/<event_id>')

if __name__ == '__main__':
    app.run(debug=True)