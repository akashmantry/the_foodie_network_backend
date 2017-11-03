from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from hashlib import md5

# initialize sql-alchemy
db = SQLAlchemy()

class Followers(db.Model):
	"""This class represents the followers table."""

	__tablename__ = 'followers'

	fid = db.Column(db.Integer, primary_key = True)
	follower_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
	followed_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)

	def __init__(self, follower_id, followed_id):
		self.follower_id = follower_id
		self.followed_id = followed_id

	def save(self):
		db.session.add(self)
		db.session.commit()

	@staticmethod
	def get_followers(id):
		return Followers.query(Followers.followed_id).filter_by(follower_id=id).all()

	@staticmethod
	def get_followers_count(id):
		return Followers.query(Followers.followed_id).filter_by(follower_id=id).all().count()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def __repr__(self):
		return "<Follower list: {}>".format(self.name)


class User(db.Model):
	"""This class represents the users table."""

	__tablename__ = 'users'

	uid = db.Column(db.Integer, primary_key = True)
	public_user_id = db.Column(db.String(100), unique = True)
	firstname = db.Column(db.String(100), nullable=False)
	lastname = db.Column(db.String(100), nullable=False)
	username = db.Column(db.String(100), unique = True, nullable=False)
	email = db.Column(db.String(100), unique = True, nullable=False)
	pwdhash = db.Column(db.String, nullable=False)
	joined_at = db.Column(default=datetime.datetime.utcnow, nullable=False)
	is_admin = db.Column(db.Boolean, default=False)
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	followed = db.relationship('Followers', 
                               foreign_keys='[Followers.follower_id]',
                               backref='followers',
                               lazy='dynamic')

	followers = db.relationship('Followers',  
                               foreign_keys='[Followers.followed_id]',
                               backref='followed',
                               lazy='dynamic')


	def __init__(self, public_user_id, firstname, lastname, username, email, password, is_admin = False):
		self.public_user_id = public_user_id
		self.firstname = firstname
		self.lastname = lastname
		self.username = username
		self.email = email.lower()
		self.is_admin = is_admin
		self.set_password(password)

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password).decode('utf-8')

	def check_password(self, password):
		print(generate_password_hash(password).decode('utf-8'))
		return check_password_hash(self.pwdhash, password)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.uid)

	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

	def is_following(self, user):
		return self.followed.filter_by(followed_id=user.uid).count() > 0
	
	def follow(self, user, session):
		if not self.is_following(user):
			newFriend = Followers(follower_id = self.uid, followed_id = user.uid)
			session.add(newFriend)
			session.commit()
			return

	def unfollow(self, user, session):
		if self.is_following(user):
			self.followed.filter_by(followed_id=user.uid).delete()
			session.commit()
			return

	def save(self):
		db.session.add(self)
		db.session.commit()

	@staticmethod
	def get_all_users():
		return User.query.all()

	@staticmethod
	def get_user_by_public_id(public_user_id):
		return User.query.filter_by(public_user_id=public_user_id).first()

	@staticmethod
	def get_user_by_firstname(firstname):
		return User.query.filter_by(firstname=firstname).all()

	@staticmethod
	def get_user_by_username(username):
		return User.query.filter_by(username=username).first()

	@staticmethod
	def get_user_by_email(email):
		return User.query.filter_by(email=email).first()

	@staticmethod
	def convert_public_user_id_to_uid(public_user_id):
		return User.query(uid).filter_by(public_user_id=public_user_id).first()

	@staticmethod
	def convert_uid_to_public_user_id(uid):
		return User.query(public_user_id).filter_by(uid=uid).first()

	@staticmethod
	def get_user_by_uid(uid):
		return User.query().filter_by(uid=uid).first()

	@staticmethod
	def get_user(filters=None):
		conditions = list()
		for attr, value in filters.items():
			conditions.append(getattr(User, attr).like("%%%s%%" % value))
		query = User.query.filter(or_(*conditions))

		return query.all()

	def delete(self, public_user_id):

		db.session.delete(self)
		db.session.commit()

	def get_followers(self):
		return self.followers

	def get_followed(self):
		return self.followed


class Post(db.Model):
	"""This class represents the users table."""

	__tablename__ = 'posts'

	pid = db.Column(db.Integer, primary_key = True)
	public_post_id = db.Column(db.String(100), unique = True)
	content = db.Column(db.String, nullable=False)
	posted_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
	public_user_id = db.Column(db.Integer, db.ForeignKey('users.public_user_id'), nullable=False)

	def __init__(self, public_post_id, content, public_user_id):
		self.public_post_id = public_post_id
		self.content = content.strip()
		self.public_user_id = public_user_id

	def save(self):
		db.session.add(self)
		db.session.commit()

	@staticmethod
	def get_all_posts(public_user_id):
		return Post.query.filter_by(public_user_id=public_user_id).all()

	@staticmethod
	def get_post_by_public_id(public_post_id):
		return Post.query.filter_by(public_post_id=public_post_id).first()

	def delete(self):
		db.session.delete(self)
		db.session.commit()
