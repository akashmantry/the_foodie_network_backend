from flask_restful import Resource, reqparse
from flask import request, jsonify, make_response
import uuid
from database.models import Post, User
from database.schema import PostSchema
import jwt
import datetime
from functools import wraps
from .util import token_required
from config import Config
from marshmallow import pprint
import re


class CreatePost(Resource):

	method_decorators = [token_required]

	def post(self, current_user):

		parser = reqparse.RequestParser(bundle_errors=True)
		parser.add_argument('content', type=str, required=True, help="Content cannot be blank!",
							 location='json')
		args = parser.parse_args()

		newPost = User(public_post_id=str(uuid.uuid4()), content=args['content'],
												public_user_id=current_user.public_user_id)
		
		newPost.save()

		return {'success': True, 'message': 'Post created'}, 204



class GetPostById(Resource):

	method_decorators = [token_required]

	def get(self, current_user, public_post_id):

		post = Post.get_post_by_public_id(public_post_id)

		if not post:
			return {'success': False, 'error_code': 13, 'message': 'No post found with this id'}, 401

		post, errors = PostSchema(only=('public_post_id', 'content', 'posted_at',
										'public_user_id').dump(post))

		if errors:
			print(errors)
			return {'success': False, 'error_code': 10, 'message':
										 'There was some error fetching the data'}, 401
		
		return post