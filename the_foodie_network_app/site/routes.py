from flask import Flask, render_template, flash, request, session, redirect, url_for
from forms import SignupForm, SigninForm, PostForm
from models import db, User, Post, Followers
from flask_login import login_user, login_required, LoginManager, logout_user, current_user
from sqlalchemy import desc
from flask_moment import Moment
import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://akash:mantry@localhost/meetneat"

db.init_app(app)
app.secret_key = "new_project"
app.debug = True

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"
moment = Moment(app)

@login_manager.user_loader
def load_user(user_id):
	return User.query.filter_by(uid = int(user_id)).first()

@app.route('/')
def index():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	return render_template('index.html')


@app.route('/signup/', methods = ['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = SignupForm()

	if request.method == 'GET':
		return render_template('signup.html', form = form)

	if request.method == 'POST':
		if form.validate() ==  False:
			return render_template('signup.html', form = form)
		else:
			firstname = form.firstname.data
			lastname = form.lastname.data
			username = form.username.data
			email = form.email.data
			password = form.password.data

			user_from_table = User.query.filter_by(username = username).first()
			email_from_table = User.query.filter_by(email = email).first()

			if user_from_table:
				print("USERNAME ALREADY PRESENT")
				flash("This username already exists.")
				return render_template('signup.html', form = form)

			if email_from_table:
				print("EMAIL ALREADY PRESENT")
				flash("This email already exists.")
				return render_template('signup.html', form = form)

			newUser = User(firstname, lastname, username, email, password)
			db.session.add(newUser)
			db.session.commit()
			login_user(newUser)
			flash("Successful signup!")
			return redirect(url_for('home'))


@app.route('/signin/', methods = ['GET', 'POST'])
def signin():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = SigninForm()

	if request.method == 'GET':
		return render_template('signin.html', form = form)

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signin.html', form = form)
		else:
			username = form.username.data
			password = form.password.data

			user_from_table = User.query.filter_by(username = username).first()

			if user_from_table:
				if user_from_table.check_password(password):
					login_user(user_from_table, remember = form.remember.data) #added
					flash("Successful signin!")
					return redirect(url_for('home'))
				else:
					flash("This password is incorrect.")
					return redirect(url_for('signin'))
			else:
				flash("This username doesn't exist.")
				return redirect(url_for('signin'))


@app.route('/signout/')
@login_required
def signout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/home/', methods = ['GET', 'POST'])
@login_required
def home():
	form = PostForm()
	posts = Post.query.order_by(desc(Post.posted_at)).limit(100).all()

	if request.method == 'GET':
		return render_template('home.html', form = form, posts = posts)

	if request.method == 'POST':
		if form.validate_on_submit() == False:
			return render_template('home.html', form = form, posts = posts)

		newPost = Post(content = form.post.data, uid = current_user.uid)
		db.session.add(newPost)
		db.session.commit()
		flash("Message posted.")
		return redirect(url_for('home'))


@app.route('/profile/<user_id>', methods = ['GET', 'POST'])
@login_required
def profile(user_id):

	user_from_table = User.query.filter_by(uid = user_id).first()
	posts_by_user = user_from_table.posts.order_by(desc(Post.posted_at))

	if request.method == 'GET':
		print("user_from_table.uid ", user_from_table.uid)
		print("current_user.followed", current_user.followed)
		return render_template('profile.html', user_from_table=user_from_table, posts_by_user=posts_by_user, current_user=current_user)

	if request.method == 'POST':
		new_friend_uid = request.form['javascript_data']
		current_user_uid = current_user.uid

		# newFriend = Followers(follower_id = current_user_uid, followed_id = new_friend_uid)
		# db.session.add(newFriend)
		# db.session.commit()
		if current_user.follow(user_from_table, db.session):
			flash(user_from_table.firstname + " added to your friend list.")
		else:
			flash("There was some problem adding " + user_from_table.firstname + " .")
		return "Friend Added"


@app.route('/add/<user_id>', methods = ['POST'])
@login_required
def add_friend(user_id):
	user_from_table = User.query.filter_by(uid = user_id).first()
	current_user_uid = current_user.uid
	if current_user.follow(user_from_table, db.session):
		flash(user_from_table.firstname + " added to your friend list.")
	else:
		flash("There was some problem adding " + user_from_table.firstname + " .")
	return redirect(url_for('profile', user_id=user_id))

@app.route('/remove/<user_id>', methods = ['POST'])
@login_required
def remove_friend(user_id):
	user_from_table = User.query.filter_by(uid = user_id).first()
	current_user_uid = current_user.uid
	if current_user.unfollow(user_from_table, db.session):
		flash(user_from_table.firstname + " removed from your friend list.")
	else:
		flash("There was some problem removing " + user_from_table.firstname + " .")
	return redirect(url_for('profile', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')


@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html')


if __name__ == "__main__":
	app.run()