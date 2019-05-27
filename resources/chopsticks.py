


from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse, fields, marshal,
                               marshal_with, url_for)

from flask_login import login_required, current_user
import models

## define what fields we want on our responses

## Marshal Fields
# chopstick_fields have to do with what we want the response object
# to the client to look like
chopstick_fields = {
    'length': fields.String,
    'width': fields.String,
    'color': fields.String,
    'message': fields.String,
    'owner': fields.String
}
#chopstick fields have to do with what we want the response object to the client to look like

# view functions
class chopstickList(Resource):
    def __init__(self):
        # reqparse, its like body-parser in express, (it makes the request object's body readable)
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument(
            'length',
            required=False,
            help='No chopstick name provided',
            location=['form', 'json']
            )

        self.reqparse.add_argument(
            'width',
            required=False,
            help='No chopstick name provided',
            location=['form', 'json']
            )

        self.reqparse.add_argument(
            'color',
            required=False,
            help='No chopstick name provided',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'message',
            required=False,
            help='No chopstick name provided',
            location=['form', 'json']
            )

        super().__init__()

    @login_required
    def get(self):


        new_chopsticks = [marshal(chopstick, chopstick_fields) for chopstick in models.chopsticks.select()]
        return new_chopsticks

    @marshal_with(chopstick_fields)
    def post(self):
        args = self.reqparse.parse_args() 
        print(args, '<----- args (req.body)')
        chopstick = models.chopsticks.create(**args)
        print(chopstick, "<---" , type(chopstick))
        return (chopstick, 201)

class chopstick(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'length',
            required=False,
            help='No chopstick name provided',
            location=['form', 'json']
            )

        self.reqparse.add_argument(
            'width',
            required=False,
            help='No chopstick name provided',
            location=['form', 'json']
            )

        self.reqparse.add_argument(
            'color',
            required=False,
            help='No chopstick name provided',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'message',
            required=False,
            help='No chopstick name provided',
            location=['form', 'json']
            )

        super().__init__()

    @marshal_with(chopstick_fields)
    def get(self, id):

        try:
            chopstick = models.chopsticks.get(models.chopsticks.id==id)
        except models.chopsticks.DoesNotExist:
            abort(404)
        else:
            return (chopstick, 200)

    @marshal_with(chopstick_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.chopstick.update(**args).where(models.chopstick.id==id)
        query.execute()
        print(query, "<--- this is query")
        return (models.chopstick.get(models.chopstick.id==id), 204)

    def delete(self, id):
        query = models.chopstick.delete().where(models.chopstick.id == id)
        query.execute()
        return {"message": "resource deleted"}


chopsticks_api = Blueprint('resources.chopsticks', __name__)

api = Api(chopsticks_api)

api.add_resource(
    chopstickList,
    '/chopsticks'
)
api.add_resource(
    chopstick,
    '/chopsticks/<int:id>'
)
