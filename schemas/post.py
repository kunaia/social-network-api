import datetime

from ma import ma
from marshmallow import post_load

from models.post import Post
from schemas.user import UserSchema


class PostSchema(ma.SQLAlchemyAutoSchema):
    author = ma.Nested(UserSchema(only=("id", "name", "surname")))

    class Meta:
        model = Post
        dump_only = ("id", "creation_date")
        include_fk = True
        load_instance = True

    @post_load
    def post_processing(self, post, *args, **kwargs):
        post.creation_date = datetime.datetime.now()
        return post
