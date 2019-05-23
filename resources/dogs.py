from flask import jsonify, Blueprint
from flask_restful import (Resource, Api, reqparse, fields, marshal,
                               marshal_with, url_for)

import models

dog_fields = {
    'id':fields.Integer,
    'name':fields.String,
    'breed':fields.String,
    'Owner':fields.String
}

# view functions
class DogList(Resource):
    def get(self):
        return jsonify({'dogs': [{'name': 'Franklin'}]})
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=false,
            help='No dog name provided',
            location=['form','json']
        )
            self.reqparse.add_argument(
            'breed',
            required=false,
            help='No dog breed provided',
            location=['form','json']
        )
            self.reqparse.add_argument(
            'owner',
            required=false,
            help='No dog owner provided',
            location=['form','json']
        )
        def post(self):
            args = self.reparse.parse_args()
            print(args,'<----args(req.body)')
            dogs = models.Dog.create(**args)
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
