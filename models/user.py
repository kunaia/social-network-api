from db import db
from models.base_model import BaseModel
from models.post import Post

from passlib.hash import sha256_crypt
from libs.abstractapi import get_geolocation, get_holiday


class User(db.Model, BaseModel):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    registration_date = db.Column(db.DateTime(timezone=True), nullable=False)
    geolocation = db.Column(db.JSON)
    coincides_holiday = db.Column(db.Boolean, default=False)

    post = db.relationship("Post", backref=db.backref("author"), lazy="dynamic")

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def verify_password(self, password):
        return sha256_crypt.verify(password, self.password)

    def set_geolocation(self, ip_address):
        self.geolocation = get_geolocation(ip_address)
        db.session.commit()

    def check_holiday(self):
        if self.geolocation:
            date = self.registration_date
            print(date)
            holiday = get_holiday(country=self.geolocation['country_code'],
                                  year=date.year,
                                  month=date.month,
                                  day=date.day)
            self.coincides_holiday = (holiday != [])
