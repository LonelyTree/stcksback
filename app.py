from flask import Flask, g
from flask_login import LoginManager
import models
from flask_cors import CORS
from resources.chopsticks import chopsticks_api
from resources.users import users_api
import config

login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id==userid)
    except models.DoesNotExist:
        return None


CORS(chopsticks_api, origins=["http://localhost:3000"], supports_credentials=True)
CORS(users_api, origins= ["http://localhost:3000"], supports_credentials=True)
app.register_blueprint(chopsticks_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/users')


@app.before_request
def before_request():

    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):

    g.db.close()
    return response



@app.route('/')
def index():
    return jsonify({"data" : "Im data"})

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)
