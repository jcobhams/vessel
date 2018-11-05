import json
from app import create_app
from app.utils import db
from app.utils.auth import Auth
from flask_testing import TestCase
from flask import current_app


class BaseTestCase(TestCase):
	
	def BaseSetUp(self):
		"""Define test variables and initialize app"""
		self.app = self.create_app()
		self.client = self.app.test_client
		
		self.migrate()
		
	@staticmethod
	def get_valid_token():
		return 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySW5mbyI6eyJpZCI6Ii1MLWtkRHpwZDRlYk1FWEFFYzdIIiwiZmlyc3RfbmFtZSI6IlZpY3RvciIsImxhc3RfbmFtZSI6IkFkdWt3dSIsImZpcnN0TmFtZSI6IlZpY3RvciIsImxhc3ROYW1lIjoiQWR1a3d1IiwiZW1haWwiOiJ2aWN0b3IuYWR1a3d1QGFuZGVsYS5jb20iLCJuYW1lIjoiVmljdG9yIEFkdWt3dSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vLTVfdXlaM0paT09vL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFjL0lUUjZOcGFWbHJnL3Bob3RvLmpwZz9zej01MCIsInJvbGVzIjp7IkZlbGxvdyI6Ii1LWEd5MUVCMW9pbWpRZ0ZpbTZDIiwiQW5kZWxhbiI6Ii1LaWloZlpvc2VRZXFDNmJXVGF1In19LCJpYXQiOjE1MzU0OTI4NTksImV4cCI6MTUzODA4NDg1OSwiYXVkIjoiYW5kZWxhLmNvbSIsImlzcyI6ImFjY291bnRzLmFuZGVsYS5jb20ifQ.MWCWnHrAM8V6kxbMClwcrFvaIUP6kuCGLS1GuQqu_aYgkJEN84C0vfAQQwzVyJLQ9TennD2k8ECRyX41RuPli8ucjMCMsI2neACJOIb2xoWwlpIExzUWMsfLkPawPki-utkQEqrcLa4vt3cR4_QQC6HZvnLa7O8g9wa52DnopPw'

	@staticmethod
	def user_id():
		return Auth.decode_token(BaseTestCase.get_valid_token())['UserInfo']['id']
	@staticmethod
	def get_invalid_token():
		return 'some.invalid.token'
		
	def create_app(self):
		"""Create the app and specify 'testing' as the environment"""
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		self.client = self.app.test_client()
		self.request_context = self.app.test_request_context()
		self.url = '/api/v1'

		@self.app.before_request
		def check_token():
			return Auth.check_token()

		@self.app.before_request
		def check_location_header():
			return Auth.check_location_header()
		
		''' Init DB'''
		
		return self.app
	
	@staticmethod
	def encode_to_json_string(data_object):
		return json.dumps(data_object)
	
	@staticmethod
	def decode_from_json_string(data_str):
		return json.loads(data_str)
	
	def make_url(self, path):
		return '{}{}'.format(self.url, path)
	
	
	@staticmethod
	def migrate():
		db.session.close()
		db.drop_all()
		db.create_all()
	
	@staticmethod
	def headers():
		return  {
			'Content-Type': 'application/json',
			'X-Location': '1',
			'Authorization': 'Bearer {}'.format(BaseTestCase.get_valid_token()),
			}
	
	@staticmethod
	def headers_without_token():
		return {
			'Content-Type': 'application/json',
			'X-Location': '1',
		}
	
	@staticmethod
	def assertJSONKeyPresent(json_object, key):
		if type(json_object) is str:
			json_obj = BaseTestCase.decode_from_json_string(json_object)
		elif type(json_object) is dict:
			json_obj = json_object
		
		if key in json_obj:
			assert True
		else:
			assert False
				
	@staticmethod
	def assertJSONKeysPresent(json_object, *keys):
		error_flag = 0
		if type(json_object) is str:
			json_obj = BaseTestCase.decode_from_json_string(json_object)
		elif type(json_object) is dict:
			json_obj = json_object
		
		for key in keys:
			
			if key not in json_obj:
				error_flag += 1
		
		if error_flag == 0:
			assert True
		else:
			assert False

