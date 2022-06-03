import os
from marshmallow import ValidationError

from flask import Flask, jsonify
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from ma import ma
from db import db

from config import Config

from models.blocklist import TokenBlocklist
from resources.user import UserRegister, UserLogin, UserLogout, UserLogout2, UserInfo
from resources.post import PostCreate, PostResource

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app)
migrate = Migrate(app, db)


# @app.before_first_request
# def create_tables():
#     db.create_all()

@app.before_first_request
def flask_migrate():
    if not os.path.exists("migrations"):
        status_code = os.system("flask db init")
    if os.system("flask db migrate") == 0:
        status_code = os.system("flask db upgrade")


# marshmallow validation error handler
@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return TokenBlocklist.is_blacklisted(jti)


# user resoirces
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserLogout2, '/logout2')
api.add_resource(UserInfo, '/user')

# post resources
api.add_resource(PostCreate, '/create_post')
api.add_resource(PostResource, '/post/<int:post_id>')

db.init_app(app)
ma.init_app(app)
if __name__ == "__main__":
    print(Config.DEBUG)
    app.run('0.0.0.0', port=5003)
