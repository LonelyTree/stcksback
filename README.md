# flask-api


#### Dependencies

```pip install flask-restful peewee```


### Setup basic server 

```python
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

```python
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

```python
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

```python
from flask import jsonify, Blueprint, abort

from flask_restful import (Resource, Api, reqparse, fields, marshal,
                               marshal_with, url_for)

import models

## define fields on responses
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
        self.reqparse.add_argument(
            'owner',
            required=False,
            help='No  owner provided',
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

- In the `__init__` function we are initializing the reqparse that will allow us to read the body of requests. We can also set requirements for the request with the `.add_argument` function with the first argument the property.  Then we can set requirements and messages back to the client if they're not meant.  

 ```python
def post(self):
        args = self.reqparse.parse_args()
        print(args, 'hittingggg ')
        dog = models.Dog.create(**args)
        return jsonify({'dogs': [{'name': 'Franklin'}]})
  ``` 
- We can access the args by calling `.parse_args` on every request, think about `body_parser` in express.  Then we are spreading out all the arguments to the properties we want to pass to the create.  An example would look like the following, 
 The location tells us where we will accept requests from in this case `x-form-www-urlencoded` and `json`, (so basically forms and ajax requests)
 
```python
>>> mydict = {'x':1,'y':2,'z':3}
>>> foo(**mydict)
x=1
y=2
z=3
```


**Test with Postman** - Select raw and create a json object and make sure to choose "JSON" as the datatype before you hit send (the drop down is where it says text)

**Formatting responses**

- So our db responses we won't be able to serialize them into json, so we have to use this thing called [marshal](marshal(data, fields, envelope=None)¶
Takes raw data (https://flask-restful.readthedocs.io/en/latest/api.html)

- marshal -Takes raw data (in the form of a dict, list, object) and a dict of fields to output and filters the data based on the fields we defined in the `dog_fields` dictionary

- This will be done to each field from our response from our database like the following

```python
def get(self):
        dogs = [marshal(dog, dog_fields)
                   for dog in models.Dog.select()]
        return {'dogs': dogs}

```

- We can also use the `marshal_with` like the following, which is just a decorator the does what we just did but for us. 

```python
@marshal_with(dog_fields)
def get(self, id):
    return dog_or_404(id)

```

- **Go ahead and use it with the Post**

```python
@marshal_with(dog_fields)
    def post(self):
        args = self.reqparse.parse_args()
        dog = models.Dog.create(**args)
        return dog
```

- and we can define a function to either send the 404 using `abort` or return the dog, and the result of that is turned in json using the `@marshal_with` decorator.  

```python
def dog_or_404(dog_id):
    try:
        dog = models.Dog.get(models.Dog.id==dog_id)
    except models.Dog.DoesNotExist:
        abort(404)
    else:
        return dog
```

### Put and Delete Route

- We have to update our class to specify what fields we want to allow on our requests to the server

```python
class Dog(Resource):
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
        self.reqparse.add_argument(
            'owner',
            required=False,
            help='No  owner provided',
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(dog_fields)
    def get(self, id):
        return dog_or_404(id)

    @marshal_with(dog_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Dog.update(**args).where(models.Dog.id==id)
        query.execute()
        return (models.Dog.get(models.Dog.id==id), 200)

```

- Here we see the put route for the model we need to define the query then execute it to perform the update, (usually it does it automatically.  Then we are just fetching the Dog and returning a tuple with a status code if we want.  You don't have to return a tuple (like we did before), but we are showing you we can and you can include the status code.  

**Go ahead and give delete a try**

```python
def delete(self, id):
    query = models.Dog.delete().where(models.Dog.id==id)
    query.execute()
    return 'resource deleted'
```

- There we go, we got a full api working!

