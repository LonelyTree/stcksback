


from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse, fields, marshal,
                               marshal_with, url_for)


import models

## define what fields we want on our responses

## Marshal Fields
dog_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'breed': fields.String,
    'owner': fields.String
}
#Dog fields have to do with what we want the response object to the client to look like

# view functions
class DogList(Resource):
    def __init__(self):
        # reqparse, its like body-parser in express, (it makes the request object's body readable)
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument(
            'name',
            required=False,
            help='No dog name provided',
            location=['form', 'json']
            )

        self.reqparse.add_argument(
            'breed',
            required=False,
            help='No dog name provided',
            location=['form', 'json']
            )

        self.reqparse.add_argument(
            'Owner',
            required=False,
            help='No dog name provided',
            location=['form', 'json']
            )

        super().__init__()

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
            'Owner',
            required=false,
            help='No dog owner provided',
            location=['form','json']
        )


    @marshal_with(dog_fields)
    def post(self):
        # read the args "req.body"
        args = self.reqparse.parse_args()
        print(args, '<----- args (req.body)')
        dog = models.Dog.create(**args)
        print(dog, "<---" , type(dog))
        # line 52 does line 54
        # dog = models.Dog.create(name=args['name'], breed=args['breed'], owner=args['owner'])
        return (dog, 201)

class Dog(Resource):
    def __init__(self):
        # reqparse, its like body-parser in express, (it makes the request object's body readable)
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument(
            'name',
            required=False,
            help='No dog name provided',
            location=['form', 'json']
            )

        self.reqparse.add_argument(
            'breed',
            required=False,
            help='No dog name provided',
            location=['form', 'json']
            )

        self.reqparse.add_argument(
            'owner',
            required=False,
            help='No dog name provided',
            location=['form', 'json']
            )

        super().__init__()

    @marshal_with(dog_fields)
    def get(self, id):

        try:
            dog = models.Dog.get(models.Dog.id==id)
        except models.Dog.DoesNotExist:
            abort(404)
        else:
            return (dog, 200)

    @marshal_with(dog_fields)
    def put(self, id):
        # parse the args (get req.body)
        args = self.reqparse.parse_args()
        query = models.Dog.update(**args).where(models.Dog.id==id)
        # we have execute the query
        query.execute()
        print(query, "<--- this is query")
        # the query doesn't respond with the update object
        return (models.Dog.get(models.Dog.id==id), 200)

    def delete(self, id):
        query = models.Dog.delete().where(models.Dog.id == id)
        query.execute()
        return{'message':'resource deleted'}

        


# were setting a module of view functions that can be attached to our flask app
dogs_api = Blueprint('resources.dogs', __name__)
#module.exports = controller

#instatiating our api from the blueprint
# gives us the special methods we can operate our api with
api = Api(dogs_api)

api.add_resource(
    DogList,
    '/dogs'
)
api.add_resource(
    Dog,
    '/dogs/<int:id>'
)
