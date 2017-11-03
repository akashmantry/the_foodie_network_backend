import unittest
import os
import json
from .. import create_app, db


class UserslistTestCase(unittest.TestCase):
	"""This class represents the users test cases"""

	def setUp(self):
		"""Define test variables and initialize app."""
		self.app = create_app(config_name="testing")
		self.client = self.app.test_client
		self.user = {'firstname': 'Barbara',
					'lastname' : 'Hanning',
					'username' : 'barbara_rocks',
					'email' : 'barbara@crap.com',
					'password' : 'barbara_rocks_123'}

		# binds the app to the current context
		with self.app.app_context():
			# create all tables
			db.create_all()

	def tearDown(self):
		"""teardown all initialized variables."""
		with self.app.app_context():
			# drop all tables
			db.session.remove()
			db.drop_all()

	def test_user_creation(self):
		"""Test API can create a user (POST request)"""
		res = self.client().post('/user/', data=self.user)
		self.assertEqual(res.status_code, 201)
		self.assertIn('Barbara', str(res.data))

	def test_api_can_get_user_by_id(self):
		"""Test API can get a single user by using it's id."""
		rv = self.client().post('/user/', data=self.user)
		self.assertEqual(rv.status_code, 201)
		result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
		result = self.client().get(
			'/user/{}'.format(result_in_json['uid']))
		self.assertEqual(result.status_code, 200)
		self.assertIn('Barbara', str(result.data))

	
	# Make the tests conveniently executable
	if __name__ == "__main__":
		unittest.main()