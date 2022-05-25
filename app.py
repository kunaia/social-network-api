import os
from marshmallow import ValidationError

from flask import Flask, jsonify
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from ma import ma
from db import db

from config import Config

from resources.user import UserRegister, UserLogin

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app)
migrate = Migrate(app, db)


@app.before_first_request
def create_tables():
    db.create_all()
# def flask_migrate():
#     if not os.path.exists("migrations"):
#         status_code = os.system("flask db init")
#     if os.system("flask db migrate") == 0:
#         status_code = os.system("flask db upgrade")


# marshmallow validation error handler
@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt = JWTManager(app)

# api resources
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, '/login')

db.init_app(app)
ma.init_app(app)
if __name__ == "__main__":
    print(Config.DEBUG)
    app.run('0.0.0.0', port=5003)
