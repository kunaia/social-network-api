import datetime

from db import db
from models.base_model import BaseModel
from models.user_post import UserPost


class Post(db.Model, BaseModel):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.String(2000), nullable=False)
    creation_date = db.Column(db.DateTime(timezone=True), nullable=False)
    last_update = db.Column(db.DateTime(timezone=True))
    like_cnt = db.Column(db.Integer, default=0)
    author_fk = db.Column(db.Integer, db.ForeignKey("user.id"))

    viewers = db.relationship('User', secondary='user_post', backref=db.backref('viewed_posts'))

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def update_body(self, new_body):
        self.body = new_body
        self.last_update = datetime.datetime.now()
        db.session.commit()
