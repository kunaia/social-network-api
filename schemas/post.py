import datetime

from ma import ma
from marshmallow import post_load, post_dump

from models.post import Post
from models.user_post import UserPost
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

    @post_dump
    def post_dump_processing(self, post_json, *args, **kwargs):
        post_json['liked'] = False
        user_id = self.context.get("user_id", None)
        if user_id:
            user_post = UserPost.find_by_user_post_ids(user_id, post_json['id'])
            post_json['liked'] = (user_post and user_post.liked)
        return post_json
