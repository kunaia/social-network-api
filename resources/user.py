from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token

from schemas.user import UserSchema
from models.user import User

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user = user_schema.load(request.get_json())
        user.set_geolocation(request.remote_addr)
        user.check_holiday()
        if user.save_to_db():
            return {"message": "user registered successfully"}, 201
        return {"message": "user with this email already exists"}, 400


class UserLogin(Resource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, required=True,
                            help="must be filled")
        parser.add_argument("password", type=str, required=True,
                            help="must be filled")
        args = parser.parse_args()

        user = User.find_by_email(args['email'])
        if user is None:
            return {"message": "user with this email not found"}, 404
        if user.verify_password(args['password']):
            access_token = create_access_token(user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       "message": "logged in",
                       "user": user_schema.dump(user),
                       "access_token": access_token,
                       "refresh_token": refresh_token
                   }, 200
        return {"message": "password is incorrect"}, 400
