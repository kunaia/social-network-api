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
    view_cnt = db.Column(db.Integer, default=0)
    author_fk = db.Column(db.Integer, db.ForeignKey("user.id"))

    viewers = db.relationship('User', secondary='user_post', backref=db.backref('viewed_posts'))

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def update_body(self, new_body):
        self.body = new_body
        self.last_update = datetime.datetime.now()
        db.session.commit()

    def viewed_by(self, user_id):
        user_post = UserPost(user_id, self.id)
        if user_post.save_to_db():
            if self.view_cnt is None:
                self.view_cnt = 0
            self.view_cnt += 1
            db.session.commit()

    def like_toggled_by(self, user_id):
        user_post = UserPost.find_by_user_post_ids(user_id, self.id)
        if user_post is not None:
            user_post.toggle_liked()
            self.like_cnt += 1 if user_post.liked else -1
            db.session.commit()
            return True
        return False
