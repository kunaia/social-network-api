from ma import ma
from datetime import datetime
from libs.abstractapi import validate_email

from passlib.hash import sha256_crypt
from marshmallow import validate, validates, post_load, ValidationError, pre_load

from models.user import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        dump_only = ("id", "registration_date")
        load_only = ("password",)
        load_instance = True

    @validates('email')
    def email_validator(self, email):
        validator = validate.Email()
        validator(email)

    @validates('password')
    def password_validator(self, password):
        if len(password) < 5:
            raise ValidationError("too short password")

    @post_load
    def post_processing(self, user, *args, **kwargs):
        user.password = sha256_crypt.hash(user.password)
        user.registration_date = datetime.now()
        return user
