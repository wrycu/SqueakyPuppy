from flask import Flask
from app.flask_app.squeaky_puppy.controllers import squeaky_puppy

app = Flask(__name__)
app.config.from_object('app.config')


@app.errorhandler(404)
def not_found(error):
    return 'Not found, bubs', 404

app.register_blueprint(squeaky_puppy)
