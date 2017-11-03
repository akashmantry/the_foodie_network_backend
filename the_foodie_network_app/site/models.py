from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from hashlib import md5
from flask import render_template


db = SQLAlchemy()


class Followers(db.Model):
	__tablename__ = 'followers'
	fid = db.Column(db.Integer, primary_key = True)
	follower_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
	followed_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)

	def __init__(self, follower_id, followed_id):
		self.follower_id = follower_id
		self.followed_id = followed_id


class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key = True)
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


	def __init__(self, firstname, lastname, username, email, password, is_admin = False):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.username = username
		self.email = email.lower()
		self.is_admin = is_admin
		self.set_password(password)

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password).decode('utf-8')

	def check_password(self, password):
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


class Post(db.Model):
	__tablename__ = 'posts'
	pid = db.Column(db.Integer, primary_key = True)
	content = db.Column(db.String, nullable=False)
	posted_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
	uid = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)

	def __init__(self, content, uid):
		self.content = content.strip()
		self.uid = uid

	def render_post(self):
		return render_template("post.html", post = self)