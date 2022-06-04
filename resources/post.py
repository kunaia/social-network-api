from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from schemas.post import PostSchema
from models.user import User
from models.user_post import UserPost
from models.post import Post


class PostCreate(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        post_schema = PostSchema()

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
        post_schema = PostSchema()

        post = Post.find_by_id(post_id)
        if post is None:
            return {"message": "post not found"}, 404
        user_id = get_jwt_identity()
        print(user_id)
        if user_id:
            post.viewed_by(user_id)
        post_schema.context["user_id"] = user_id
        return {"post": post_schema.dump(post)}, 200

    @classmethod
    @jwt_required()
    def put(cls, post_id):
        post_schema = PostSchema()

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


class PostLike(Resource):
    @classmethod
    @jwt_required()
    def post(cls, post_id):
        user_id = get_jwt_identity()
        post = Post.find_by_id(post_id)
        if post is None:
            return {"message": "post not found"}, 404
        user_post = UserPost.find_by_user_post_ids(user_id, post_id)
        if user_post is None:
            return {"message": "Bad Request, You have not viewed post yet"}, 400

        if post.like_toggled_by(user_id):
            return {"message": "changed successfully"}, 200
        return {"message": "problem occurred"}, 500


class PostsResource(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls):
        posts_schema = PostSchema(many=True)
        posts_schema.context['user_id'] = get_jwt_identity()

        posts = Post.get_all()
        return {"posts": posts_schema.dump(posts)}
