from tests.base_test_case import BaseTestCase
from app.utils.auth import Auth

class TestAuth(BaseTestCase):
	
	def setUp(self):
		self.BaseSetUp()
	
	def test_get_user_method_return_dict_of_user_data_if_valid_header_present(self):
		
		with self.app.test_request_context(path='/api/v1/vendors', method='GET', headers=self.headers()) as request:
			user_data = Auth._get_user()
			
			self.assertIsInstance(user_data, dict)
			self.assertIsNotNone(user_data)
			self.assertJSONKeysPresent(user_data, 'id', 'first_name', 'last_name', 'email')
	
	def test_user_method_return_list_of_user_data_based_on_supplied_keys(self):
		
		with self.app.test_request_context(path='/api/v1/vendors', method='GET', headers=self.headers()) as request:
			decoded = Auth.decode_token(self.get_valid_token())
			
			values = Auth.user('id', 'first_name', 'last_name', 'email')
			id, first_name, last_name, email = values
			
			self.assertIsInstance(values, list)
			self.assertEquals(decoded['UserInfo']['id'], id)
			self.assertEquals(decoded['UserInfo']['first_name'], first_name)
			self.assertEquals(decoded['UserInfo']['last_name'], last_name)
			self.assertEquals(decoded['UserInfo']['email'], email)
	
	def test_get_token_throws_exception_when_auth_header_missing(self):
		try:
			Auth.get_token()
			assert False
		except Exception as e:
			assert True
	
	def test_get_token_return_token_if_valid_header_present(self):
		
		with self.app.test_request_context(path='/api/v1/vendors', method='GET', headers=self.headers()) as request:
			token = Auth.get_token()
			
			self.assertIsInstance(token, str)
			self.assertIsNotNone(token)
			
			
	def test_decode_token_throws_exception_on_invalid_token(self):
		try:
			Auth.decode_token(self.get_invalid_token())
			assert False
		except Exception as e:
			assert True
	
	def test_decode_token_returns_dict_on_valid_token(self):
		token = Auth.decode_token(self.get_valid_token())
		if type(token) is dict:
			assert True
		else:
			assert False
			
	def test_get_location_throws_exception_when_location_header_missing(self):
		try:
			Auth.get_location()
			assert False
		except Exception as e:
			assert True
			
	def test_get_location_header_returns_int_value_when_location_header_present(self):
		with self.app.test_request_context(path='/api/v1/vendors', method='GET', headers=self.headers()) as request:
			location = Auth.get_location()
			self.assertIsInstance(location, int)
			self.assertIsNotNone(location)
			