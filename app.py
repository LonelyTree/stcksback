from flask import Flask, g

import models

# because we have __init__.py we can use the folder as module
from resources.dogs import dogs_api



DEBUG = True
PORT = 8000

app = Flask(__name__)
# app.use(dogController, '/api/v1')
# url prefix start every route with /api/v1 in that blue print
app.register_blueprint(dogs_api, url_prefix='/api/v1')


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
    app.run(debug=DEBUG, port=PORT)
