from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from schemas.post import PostSchema
from models.user import User
from models.post import Post

post_schema = PostSchema()
posts_schema = PostSchema(many=True)


class PostCreate(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        data = request.get_json()
        data["author_fk"] = get_jwt_identity()
        post = post_schema.load(data)
        if post.save_to_db():
            return {"message": "created successfully"}, 201
        return {"message": "error while saving to db"}, 500


class PostResource(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls, post_id):
        post = Post.find_by_id(post_id)
        if post is None:
            return {"message": "post not found"}, 404
        return {"post": post_schema.dump(post)}, 200

    @classmethod
    @jwt_required()
    def put(cls, post_id):
        post = Post.find_by_id(post_id)
        if post is None:
            return {"message": "post not found"}, 404
        if post.author_fk != get_jwt_identity():
            return {"message": "you don't own this post"}, 403

        new_post = post_schema.load(request.get_json())
        post.update_body(new_post.body)
        return {"message": "updated successfully"}, 200

    @classmethod
    @jwt_required()
    def delete(cls, post_id):
        post = Post.find_by_id(post_id)
        if post is None:
            return {"message": "post not found"}, 404
        if post.author_fk != get_jwt_identity():
            return {"message": "you don't own this post"}, 403

        if post.remove_from_db():
            return {"message": "post removed successfully"}, 200
        return {"message": "some problem occurred while removing"}, 500
