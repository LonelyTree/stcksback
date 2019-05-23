from flask import jsonify, Blueprint
from flask_restful import Resource, Api

import models

# view functions
class DogList(Resource):
    def get(self):
        return jsonify({'dogs': [{'name': 'Franklin'}]})


class Dog(Resource):
    def get(self, id):
        return jsonify({'name': 'Franklin'})

    def put(self, id):
        return jsonify({'name': 'Franklin'})

    def delete(self, id):
        return jsonify({'name': 'Franklin'})

dogs_api = Blueprint('resources.dogs', __name__)

#app.use(dogController, 'dogs')

api = Api(dogs_api)

api.add_resource(
    DogList,
    '/dogs',
    endpoint='dogs'
)
api.add_resource(
    Dog,
    '/dogs/<int:id>',
    endpoint='dog'
)
