from flask_restful import Resource, reqparse
from flask import request, jsonify, make_response
import uuid
from the_foodie_network_app.database.models import User
from the_foodie_network_app.database.schema import UserSchema
import jwt
import datetime
from functools import wraps
from .util import token_required
from the_foodie_network_app.config import Config
from marshmallow import pprint
import re


def authorize_user(func):
	@wraps(func)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not auth.username or not auth.password:
			return {'success': False, 'error_code': 1, 'message': 'Login required'}, 401
		
		return func(*args, **kwargs)
	return decorated


class Authenticate(Resource):
	method_decorators = [authorize_user]


class UserLogin(Authenticate):

	def post(self):
		user = User.get_user_by_username(request.authorization.username)

		if not user:
			return {'success': False, 'error_code': 2, 'message': 'Incorrect username'}, 401

		if user.check_password(request.authorization.password):
		# generate token
			try:
				payload = {
					'public_user_id': user.public_user_id,
					'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
					'iat': datetime.datetime.utcnow()
				}
				token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

				return {'token': token.decode('UTF-8')}

			except Exception as e:
				print(e)

		return {'success': False, 'error_code': 2, 'message': 'Incorrect password'}, 401


class UserSignup(Resource):

	def post(self):

		parser = reqparse.RequestParser(bundle_errors=True)
		parser.add_argument('firstname', type=str, required=True, help="First name cannot be blank!",
							 location='json')
		parser.add_argument('lastname', type=str, required=True, help="Last name cannot be blank!",
							 location='json')
		parser.add_argument('username', type=str, required=True, help="Username cannot be blank!",
							 location='json')
		parser.add_argument('email', type=str, required=True, help="Email cannot be blank!",
							 location='json')
		parser.add_argument('password', type=str, required=True, help="Password cannot be blank!",
							 location='json')
		args = parser.parse_args()

		user = User.get_user_by_username(args['username'])
		if user:
			return {'success': False, 'error_code': 8, 'message': 'Username already registered'}, 401

		user = User.get_user_by_email(args['email'])
		if user:
			return {'success': False, 'error_code': 8, 'message': 'Email already registered'}, 401

		newUser = User(public_user_id=str(uuid.uuid4()), firstname=args['firstname'],
												lastname=args['lastname'],
												username=args['username'],
												email=args['email'],
												password=args['password'])
		
		newUser.save()

		#TODO Generate token
		return {'success': True, 'message': 'User created'}, 204


# SEARCH FUNCTIONALITY

class GetAllUsers(Resource):
	"""
	This is crap!
	Change it to something useful once I find what that 'useful' is!!!
	"""

	method_decorators = [token_required]

	def get(self, current_user):
		if not current_user.is_admin:
			return {'success': False, 'error_code': 3, 'message': 'You are not an admin'}, 401

		users = User.get_all_users()
		users, errors = UserSchema(only=('public_user_id', 'firstname', 'lastname',
										'username', 'email', 'joined_at', 'posts',
										'followers', 'followed'),
										 many=True).dump(users)

		if errors:
			print(errors)
			return {'success': False, 'error_code': 10, 'message':
										 'There was some error fetching the data'}, 401
		
		return users


class UserById(Resource):
	"""
	Searches using public user id.
	"""
	method_decorators = [token_required]

	def get(self, current_user, user_public_user_id):

		user = User.get_user_by_public_id(user_public_user_id)
		
		if not user:
			return {'success': False, 'error_code': 7, 'message': 'No user found with this id'}, 401

		user, errors = UserSchema(only=('public_user_id', 'firstname', 'lastname',
										'username', 'email', 'joined_at', 'posts',
										'followers', 'followed')).dump(user)

		if errors:
			print(errors)
			return {'success': False, 'error_code': 10, 'message':
										 'There was some error fetching the data'}, 401
		
		return user


class SearchUser(Resource):
	"""
	Searches username, firstname, lastname and email - all in one.
	It can even search partial names, like 'akas' for 'akash'.
	"""

	method_decorators = [token_required]

	def get(self, current_user, name):
		firstname = None
		lastname = None
		email = None
		username = None

		words = name.split('+')
		if len(words) > 2:
			firstname = words[0] + " " + words[1]
			lastname = ''.join(word for word in words[2:])

		if len(words) == 2:
			firstname = words[0]
			lastname = words[1]

		if len(words) == 1:
			if re.match("[^@]+@[^@]+\.[^@]+", words[0]):
				email = words[0]
			else:
				firstname = words[0]
				lastname = words[0]
				username = words[0]

		filters = {}
		if firstname:
			filters['firstname'] = firstname
		if lastname:
			filters['lastname'] = lastname
		if username:
			filters['username'] = username
		if email:
			filters['email'] = email

		matches = User.get_user(filters)
		print(matches)
		if not matches:
			return {'success': False, 'error_code': 7, 'message': 'No user found with this name'}, 401

		users, errors = UserSchema(only=('public_user_id', 'firstname', 'lastname',
										'username', 'email', 'joined_at', 'posts',
										'followers', 'followed'), 
										many=True).dump(matches)

		print(users)
		if errors:
			print(errors)
			return {'success': False, 'error_code': 10, 'message':
										 'There was some error fetching the data'}, 401
		
		return users

