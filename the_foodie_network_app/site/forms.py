from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
	firstname = StringField("Firstname", validators = [DataRequired("Fistname required."), Length(min=1, max=100)])
	lastname = StringField("Lastname", validators = [DataRequired("Lastname required."), Length(min=1, max=100)])
	username = StringField("Username", validators = [DataRequired("Username required."), Length(min=1, max=100)])
	email = StringField("Email", validators = [DataRequired("Email required."), Email("Enter valid email."), Length(min=4, max=100)])
	password = PasswordField("Password", validators = [DataRequired("Password required."), Length(min=6, max=100, message="Password must be atleast 6 characters long.")])
	submit = SubmitField("Sign Up")

class SigninForm(FlaskForm):
	username = StringField("Username", validators = [DataRequired("Username required."), Length(min=4, max=100)])
	password = PasswordField("Password", validators = [DataRequired("Password required."), Length(min=6, max=100, message="Password must be atleast 6 characters long.")])
	remember = BooleanField('Remember me')
	submit = SubmitField("Signin")

class PostForm(FlaskForm):
	post = TextAreaField("What's up?", validators = [DataRequired("Content required to post.")])
	submit = SubmitField("Post")
