# flask-api

We are going to create a basic api that performs all crud routes, as well as have using registration and session setup



#### Setup virtualenv

- inside flask-api-dogs folder
```bash
virtualenv .env -p python3
source .env/bin/activate
```

#### Dependencies

```
pip3 install flask-restful peewee flask psycopg2 flask_login flask_cors
pip3 freeze > requirements.txt
```


### Setup basic server 

```python
from flask import Flask

DEBUG = True
PORT = 8000

app = Flask(__name__)


@app.route('/')
def index():
    return 'hi'

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
```

### models.py


```python
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

- We are using sqlite as our database here, this is really great for development purposes to get up and running real quick, later on we will connect to our production database postgres.

- Meta - When Python creates a class object, special construction instructions can be provided. This is done through the Meta class. In this case, the Model base class includes methods for creating and saving instances of this class to a database. This requires knowing which database to use. Since the database isn't part of the class itself, this class constructor information is provided through the special Meta class.

- The initialize method will set up our datatables, while we open and close the connection

### Update the app.py

```python
from flask import Flask, g

import models

DEBUG = True
PORT = 8000

app = Flask(__name__)


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

@app.route('/')
def index():
    return 'hi'


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
```

- the `g` stands for global and we are setting up a global access to our database throughout the app. 

- when developing a web application, it’s common to open a connection when a request starts, and close it when the response is returned. You should always manage your connections explicitly. For instance, if you are using a connection pool, connections will only be recycled correctly if you call connect() and close().

We will tell flask that during the request/response cycle we need to create a connection to the database. Flask provides some useful decorators to make this easy

```python
@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response
 ```

### resources 

```bash
mkdir resources
touch resources/init.py
touch resources/dogs.py
```

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


**Test with Postman** - Select raw and create a json object and make sure to choose "JSON" as the datatype before you hit send (the drop down is where it says text), here's an object you can use

```json
{
	"name": "Frankie",
	"breed": "newfie",
	"owner": "Jim"
}
```

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

### Adding Users

- Lets add a user model 


```python
import datetime

from peewee import *
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

import config

DATABASE = SqliteDatabase('dogs.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        email = email.lower()
        try:
            cls.select().where(
                (cls.email==email)
            ).get()
        except cls.DoesNotExist:
            user = cls(username=username, email=email)
            user.password = generate_password_hash(password)

            user.save()
            return user
        else:
            raise Exception("User with that email already exists")

class Dog(Model):
    name = CharField()
    owner = CharField()
    breed = CharField()
    created_by = ForeignKeyField(User, related_name='dog_set')
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Dog], safe=True)
    DATABASE.close()

```

- This is very similar to what we did on Friday, and we added a relation with the Dog model.  

- Notice we can also create a `config` file to hold our configuration options.  

```python
DEBUG = True
PORT = 8000
SECRET_KEY = 'jasdlfj.adsfjlajdsf.adsjflkadsf'
```

- then just update the `app.py`

```python
from flask import Flask

import models
from resources.users import users_api
from resources.dogs import dogs_api
from flask_cors import CORS
from flask_login import LoginManager
login_manager = LoginManager()
## sets up our login for the app


import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

CORS(dogs_api, origins=["http://localhost:3000"], supports_credentials=True)
CORS(users_api, origins= ["http://localhost:3000"], supports_credentials=True)
app.register_blueprint(dogs_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/api/v1')

@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)
    
```


- `config.secretkey` is for the hash for our session cookie we can make up whatever random characters we'd like. By default, Flask-Login uses sessions for authentication. This means you must set the secret key on your application,

-  We can use the `LoginManager()` to handle all the login things like is_authenticated, or get id. The login manager contains the code that lets your application and Flask-Login work together, such as how to load a user from an ID, and where to send users when they need to log in.  

-  `@login_manager.user_loader` - We need to provide user_loader callback. This callback is used to reload the user object from the user ID stored in the session. It should take the unicode ID of a user, and return the corresponding user object.


- We also set up the login manager and setup cors to allow our react app to connect to our API's.  Notice we passed `supports_credentials=True` as well in order to give us the ability to send cookies back and forth.  

- So we defined the `users_api` lets go ahead and write the routes out. 

```python
import json

from flask import jsonify, Blueprint, abort, make_response

from flask_restful import (Resource, Api, reqparse,
                               inputs, fields, marshal,
                               marshal_with, url_for)

from flask_login import login_user, logout_user, login_required, current_user
import models

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
        if args['password'] == args['verify_password']:
            print(args, ' this is args')
            user = models.User.create_user(**args)
            login_user(user)
            return marshal(user, user_fields), 201
        return make_response(
            json.dumps({
                'error': 'Password and password verification do not match'
            }), 400)



users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    UserList,
    '/users',
    endpoint='users'
)
```


- Now we can just add `@login_required` wherever we want as a decorator

```python
@login_required
def get(self):

    dogs = [marshal(dog, dog_fields)
               for dog in models.Dog.select()]
    return {'dogs': dogs}

```

Cool and we've set up our api to work with react!


### Setting up Postgres

```sql
$ psql
> CREATE DATABASE database_name;
> CREATE USER jimuser WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE dog TO jimuser;
> \q
```

- We have to create our db on our computer.  

- Then we just update our database.

models.py
```python
DATABASE = PostgresqlDatabase(
    'dog',  # Required by Peewee.
    user='jim',  # Will be passed directly to psycopg2.
    password='password'
    )  

```





