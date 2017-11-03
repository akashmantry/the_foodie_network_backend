from flask import Flask, Blueprint
from flask_restful import Api
from the_foodie_network_app.resources.user import UserLogin, GetAllUsers, UserById, UserSignup, SearchUser
from the_foodie_network_app.config import app_config
from the_foodie_network_app.database.models import db


app = Flask(__name__)
api_blue_print = Blueprint('api', __name__)

config_name = 'development'
app.config.from_object(app_config[config_name])

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

api = Api(api_blue_print)
api.add_resource(UserLogin, '/v1/login')
api.add_resource(GetAllUsers, '/v1/users')
api.add_resource(UserById, '/v1/users/id/<string:user_public_user_id>',
							'/v1/users/firstname/<string:user_firstname>',
							'/v1/users/lastname/<string:user_lastname>',
							'/v1/users/username/<string:user_username>',
							'/v1/users/email/<string:user_email>')
api.add_resource(SearchUser, '/v1/users/search/<string:name>')
api.add_resource(UserSignup, '/v1/signup')
app.register_blueprint(api_blue_print, url_prefix='/api')

app.run()





# @mod.route('/users', methods=['GET'])
# @token_required
# def get_all_users(current_user):

# 	if not current_user.is_admin:
# 		return jsonify({'message': 'Cannot perform this function'})

# 	users = User.get_all_users()
# 	user_list = list()
# 	for user in users:
# 		user_data = dict()
# 		user_data['public_user_id'] = user.public_user_id
# 		user_data['firstname'] = user.firstname
# 		user_data['lastname'] = user.lastname
# 		user_data['username'] = user.username
# 		user_data['email'] = user.email

# 		user_list.append(user_data)
# 	return jsonify({'users': user_list})

# @mod.route('/user/<user_public_user_id>', methods=['GET'])
# @token_required
# def get_user_by_id(current_user, user_public_user_id):

# 	user = User.get_user_by_public_id(user_public_user_id)
# 	if not user:
# 		return jsonify({'message': 'No user found'})

# 	user_data = dict()
# 	user_data['public_user_id'] = user.public_user_id
# 	user_data['firstname'] = user.firstname
# 	user_data['lastname'] = user.lastname
# 	user_data['username'] = user.username
# 	user_data['email'] = user.email
# 	user_data['joined_at'] = user.joined_at

# 	user_data['posts'] = list()
# 	for post in user.posts:
# 		post_data = dict()
# 		post_data['public_post_id'] = post.public_post_id
# 		post_data['content'] = post.content
# 		post_data['posted_at'] = post.posted_at
# 		user_data['posts'].append(post_data)

# 	user_data['followers'] = list()
# 	for follower in user.followers:
# 		follower_data = dict()
# 		follower_data['public_user_id'] = follower.public_user_id
# 		follower_data['firstname'] = follower.firstname
# 		follower_data['lastname'] = follower.lastname
# 		user_data['followers'].append(follower_data)

# 	user_data['followed'] = list()
# 	for followed in user.followed:
# 		followed_data = dict()
# 		followed_data['public_user_id'] = followed.public_user_id
# 		followed_data['firstname'] = followed.firstname
# 		followed_data['lastname'] = followed.lastname
# 		user_data['followed'].append(followed_data)

# 	return jsonify({'user': user_data})

# @mod.route('/user', methods=['POST'])
# @token_required
# def create_user(current_user):
# 	data = request.get_json()
# 	newUser = User(public_user_id=str(uuid.uuid4()), firstname=data['firstname'],
# 												lastname=data['lastname'],
# 												username=data['username'],
# 												email=data['email'],
# 												password=data['password'])
# 	newUser.save()
# 	return jsonify({'message': 'New user created.'})

# @mod.route('/user/<user_id>', methods=['PUT'])
# @token_required
# def change_user(current_user, id):
# 	return

# @mod.route('/user/<user_public_user_id>', methods=['DELETE'])
# @token_required
# def delete_user(current_user, user_public_user_id):

# 	if not current_user.is_admin:
# 		return jsonify({'message': 'Cannot perform this function'})

# 	user = User.get_user_by_public_id(user_public_user_id)
	
# 	if not user:
# 		return jsonify({'message': 'No user found'})

# 	user.delete()
# 	return jsonify({'message': 'User deleted'})


# @mod.route('/post', methods=['POST'])
# @token_required
# def create_post(current_user):
# 	data = request.get_json()
# 	user_uid = User.convert_public_id_to_uid(current_user.public_user_id)
# 	newPost = Post(public_post_id=str(uuid.uuid4()), content=data['content'], uid=user_uid)
# 	newPost.save()
# 	return jsonify({'message': 'New post created.'})

# @mod.route('/posts/<user_public_user_id>', methods=['GET'])
# @token_required
# def get_all_posts_of_user(current_user, user_public_user_id):

# 	user_uid = User.convert_public_id_to_uid(user_public_user_id)
# 	posts = Post.get_all_posts(user_uid)

# 	post_list = list()
# 	for post in posts:
# 		post_data = dict()
# 		post_data['public_post_id'] = post.public_user_id
# 		post_data['content'] = post.content
# 		post_data['posted_at'] = post.posted_at
# 		post_data['uid'] = post.uid
		
# 		post_list.append(post_data)

# 	return jsonify({'posts': post_list})

# @mod.route('/post/<post_public_post_id>', methods=['GET'])
# @token_required
# def get_post_by_id(current_user, user_public_user_id):

# 	post = Post.get_post_by_id(post_public_post_id)

# 	if not post:
# 		return jsonify({'message': 'No post found'})

# 	user = User.get_user_by_uid(post.uid)

# 	post_data = dict()
# 	post_data['public_post_id'] = post.public_user_id
# 	post_data['content'] = post.content
# 	post_data['posted_at'] = post.posted_at
# 	post_data['firstname'] = user.firstname
# 	post_data['lastname'] = user.lastname

# 	return jsonify({'post': post_data})

# @mod.route('/post/<post_public_post_id>', methods=['PUT'])
# @token_required
# def edit_post_by_id(current_user, user_public_user_id):

# 	post = Post.get_post_by_id(post_public_post_id)

# 	if not post:
# 		return jsonify({'message': 'No post found'})

# 	user_uid = User.convert_public_id_to_uid(current_user.public_user_id)

# 	if post.uid != user_uid:
# 		return jsonify({'message': "You don't have the permisson to edit this post"})

# 	data = request.get_json()

# 	public_user_id = post.public_user_id

# 	post.delete()

# 	newPost = Post(public_post_id=post.public_user_id, content=data['content'], uid=user_uid)
# 	newPost.save()
# 	return jsonify({'message': 'Post edited successfully.'})

# @mod.route('/post/<post_public_post_id>', methods=['DELETE'])
# @token_required
# def delete_post(current_user, post_public_user_id):

# 	post = Post.get_post_by_id(post_public_post_id)
# 	user_uid = User.convert_public_id_to_uid(current_user.public_user_id)

# 	if post.uid != user_uid:
# 		return jsonify({'message': "You don't have the permisson to delete this post"})

# 	post.delete()

# 	return jsonify({'message': 'Post deleted'})

