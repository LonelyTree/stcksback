# flask-api


#### Dependencies

```pip install flask-restful peewee```


### Setup basic server 

```
from flask import Flask

DEBUG = True
PORT = 8000

app = Flask(__name__)



@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
```

### models.py


```
import datetime

from peewee import *

DATABASE = SqliteDatabase('dogs.sqlite')


class Dog(Model):
    name = CharField()
    owner = CharField()
    breed = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE




def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Dog], safe=True)
    DATABASE.close()

```


### resources 

```
from flask import jsonify, Blueprint

from flask_restful import Resource, Api

import models


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
```

*Whats a resource?* - The main building block provided by Flask-RESTful are resources, which gives us access our HTTP methods just by defining methods on your resource. A basic crud source looks like above.  

*jsonify* - turning our python dictionaries into json.  

-  *BluePrints* - The basic concept of blueprints is that they record operations to execute when registered on an application. Flask associates view functions with blueprints when dispatching requests and generating URLs from one endpoint to another.

- `dogs_api = Blueprint('resources.dogs', __name__)` says treat this as a blueprint in the application (module) that we can attach to our flask app the will define a set of view functions.  

- `api = Api(dogs_api)` - This is instating our api from our blueprint (or an app), that gives us special methods we can work with to operate our api.  Docs can be found [here](https://flask-restful.readthedocs.io/en/latest/api.html#id1)

- In the `add_resource` - the first argument is the class to construct the end points, and the second argument is the endpoint for the url.

**Now we need to Register the Blueprint in the app**

```
from flask import Flask

import models
from resources.dogs import dogs_api


DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

app = Flask(__name__)
app.register_blueprint(dogs_api, url_prefix='/api/v1')

## rest of file

```

- the `url_prefix='/api/v1'` is prefix all of our routes (`/dogs`, `/dogs/<int:id>`) with `/api/v1`


### Reqparse 

- It’s designed to provide simple and uniform access to any variable on the flask.request object in Flask.

- This will allow us the build out what our requests should look like and give us ability to respond to errors easily, this is much like forms.  

- Lets refactor our classes like the following 

```
from flask import jsonify, Blueprint

from flask_restful import Resource, Api, reqparse, fields

import models

## define fields on requests
dog_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'breed': fields.String,
}


class DogList(Resource):
    def __init__(self):
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
            help='No course dog breed provided',
            location=['form', 'json']
        )
        super().__init__()
    def get(self):
        return jsonify({'dogs': [{'name': 'Franklin'}]})

    def post(self):
        args = self.reqparse.parse_args()
        print(args, 'hittingggg ')
        dog = models.Dog.create(**args)
        return jsonify({'dogs': [{'name': 'Franklin'}]})


class Dog(Resource):
    def get(self, id):
        return jsonify({'name': 'Franklin'})

    def put(self, id):
        return jsonify({'name': 'Franklin'})

    def delete(self, id):
        return jsonify({'name': 'Franklin'})

dogs_api = Blueprint('resources.dogs', __name__)
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
```

- In the `__init__` function we are initializing the reqparse that will allow us to read the body of requests. We can also set requirements for the request with the `.add_argument` function with the first argument being one of the properties defined in the `dog_fields` dictionary at the top.  Then we can set requirements and messages back to the client if they're not meant.  

 ```
def post(self):
        args = self.reqparse.parse_args()
        print(args, 'hittingggg ')
        dog = models.Dog.create(**args)
        return jsonify({'dogs': [{'name': 'Franklin'}]})
  ``` 
- We can access the args by calling `.parse_args` on every request, think about `body_parser` in express.  Then we are spreading out all the arguments to the properties we want to pass to the create.  An example would look like the following, 

```
>>> mydict = {'x':1,'y':2,'z':3}
>>> foo(**mydict)
x=1
y=2
z=3
```
