from db import db
from models.base_model import BaseModel


class UserPost(db.Model, BaseModel):
    __tablename__ = "user_post"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="RESTRICT"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    liked = db.Column(db.Boolean, default=False)
    db.UniqueConstraint(user_id, post_id)

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id

    @classmethod
    def find_by_user_post_ids(cls, user_id, post_id):
        return cls.query.filter_by(user_id=user_id, post_id=post_id).first()

    def toggle_liked(self):
        self.liked = not self.liked
        db.session.commit()
