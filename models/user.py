from db import db
from models.base_model import BaseModel

from passlib.hash import sha256_crypt


class User(db.Model, BaseModel):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def verify_password(self, password):
        return sha256_crypt.verify(password, self.password)
