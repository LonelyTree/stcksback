from flask import Flask, g
from flask_login import LoginManager
import models
from flask_cors import CORS
# because we have __init__.py we can use the folder as module
from resources.dogs import dogs_api
from resources.users import users_api
import config

# sets up the login for the app
login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# this sets up our session and everything
login_manager.init_app(app)

# define a function to load the user when we
# want to access them in our session
# this is the callback to load the user from the sessin
# the userid is stored in the session when they login
@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id==userid)
    except models.DoesNotExist:
        return None

# app.use(dogController, '/api/v1')
# url prefix start every route with /api/v1 in that blue print
CORS(dogs_api, origins=["http://localhost:3000"], supports_credentials=True)
CORS(users_api, origins= ["http://localhost:3000"], supports_credentials=True)
app.register_blueprint(dogs_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/users')


@app.before_request
def before_request():
    # g is global object
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response



@app.route('/')
def index():
    return jsonify({"data" : "Im data"})

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)
