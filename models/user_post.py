from db import db
from models.base_model import BaseModel


class UserPost(db.Model, BaseModel):
    __tablename__ = "user_post"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_fk = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="RESTRICT"), nullable=False)
    post_fk = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    liked = db.Column(db.Boolean, default=False)
    db.UniqueConstraint(user_fk, post_fk)

    def __init__(self, user_id, post_id):
        self.user_fk = user_id
        self.post_fk = post_id
