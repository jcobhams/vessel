from tests.base_test_case import BaseTestCase

class TestDummyEndpoints(BaseTestCase):
	'''
	You can delete or modify this file if you want.
	It's purpose is to show how to write tests for controller endpoints.
	
	No Actual CRUD operations happen.
	
	'''

	def setUp(self):
		self.BaseSetUp()

	def test_create_dummy_endpoint(self):
		
		dummy = {'id': 1, 'name': 'Joseph Cobhams', 'stacks': ['Python', 'PHP', 'GO']}
	
		# Make Post Request Like This
		# response = self.client().post(self.make_url('/dummy/user/profile'), data=self.encode_to_json_string(dummy), headers=self.headers())

		# Get Response JSON and perform assertions.
		# response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		# payload = response_json['payload']


		# self.assertEqual(response.status_code, 201)
		# self.assertJSONKeyPresent(response_json, 'payload')
		# self.assertEqual(payload['user']['id'], dummy['id'])
		# self.assertEqual(payload['user']['name'], dummy['name'])
		
		# GET Requests
		# response = self.client().get(self.make_url(f'/dummy/user/{user_id}'), headers=self.headers())
		
		
		
		# Assert True just so this dummy tests passes
		self.assertTrue(True)