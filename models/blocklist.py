from db import db
from models.base_model import BaseModel

from config import Config
from datetime import datetime


class TokenBlocklist(db.Model, BaseModel):
    __tablename__ = "blocklist"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(100), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, token, token_type):
        self.token = token
        self.token_type = token_type
        self.date = datetime.utcnow()

    @classmethod
    def is_blacklisted(cls, token):
        return cls.query.filter_by(token=token).first() is not None

    def add_to_blacklist(self):
        self.save_to_db()

    @classmethod
    def delete_expired_tokens(cls):
        cls.query.filter(cls.token_type == 'access',
                         datetime.utcnow() - cls.date > Config.JWT_ACCESS_TOKEN_EXPIRES).delete()
        db.session.commit()
