from marshmallow import Schema, fields, post_load
from the_foodie_network_app.database.models import User, Post


class PostSchema(Schema):
		
	pid = fields.Integer()
	public_post_id = fields.Str()
	content = fields.Str()
	posted_at = fields.DateTime()
	public_user_id = fields.Str()

	@post_load
	def make_user(self, data):
		return Post(**data)


class UserSchema(Schema):
		
	uid = fields.Integer()
	public_user_id = fields.Str()
	firstname = fields.Str()
	lastname = fields.Str()
	username = fields.Str()
	email = fields.Str()
	pwdhash = fields.Str()
	joined_at = fields.DateTime()
	isAdmin = fields.Bool()
	posts = fields.Nested(PostSchema)
	followed = fields.Nested('self', many=True)
	followers = fields.Nested('self', many=True)

	@post_load
	def make_user(self, data):
		return User(**data)



 	