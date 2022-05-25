from ma import ma
from libs.abstractapi import validate_email

from passlib.hash import sha256_crypt
from marshmallow import validate, validates, post_load, ValidationError

from models.user import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        dump_only = ("id",)
        load_only = ("password",)
        load_instance = True

    @validates('email')
    def email_validator(self, email):
        if not validate_email(email):
            raise ValidationError("Not valid email address")

    @validates('password')
    def password_validator(self, password):
        if len(password) < 5:
            raise ValidationError("too short password")

    @post_load
    def encrypt_password(self, data, *args, **kwargs):
        data["password"] = sha256_crypt.hash(data['password'])
        return data
