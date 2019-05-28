import json

from flask import jsonify, Blueprint, abort, make_response, Flask, g

from flask_restful import (Resource, Api, reqparse,
                               inputs, fields, marshal,
                               marshal_with, url_for)

from flask_login import login_user, logout_user, login_required, current_user
import models
from flask_bcrypt import check_password_hash


app = Flask(__name__)

user_fields = {
    'username': fields.String,
}


class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'verify_password',
            required=True,
            help='No password verification provided',
            location=['form', 'json']
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        print(args)
        if args['password'] == args['verify_password']:
            print(args, ' this is args')
            user = models.User.create_user(**args)
            login_user(user)

            return marshal(user, user_fields), 201
        return make_response(
            json.dumps({
                'error': 'Password and password verification do not match'
            }), 400)

 


class UserLogin(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No email provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided.',
            location=['form', 'json']
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        try:
            logged_user = models.User.get(models.User.username == args['username'])
            print('---------- logged')
        except models.DoesNotExist:
            print('User does not exist!')
            return 'User does not exist!'
        else:
            if logged_user and check_password_hash(logged_user.password, args['password']):
                login_user(logged_user)
                print(current_user)
                print('current_user')
                return marshal(logged_user, user_fields)
            else:
                return 'Your email or password doesn\'t match!'

class UserLogout(Resource):
    @login_required
    def get(self):
        logout_user()
        print('User has been successfully logged out.')
        return 'User has been successfully logged out.'



users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    UserList,
    '/registration'
)
api.add_resource(
    UserLogin,
    '/login',
    endpoint='userslogin'
)

api.add_resource(
    UserLogout,
    '/logout',
    endpoint='userslogout'
)
