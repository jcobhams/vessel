from app.utils.auth import Auth
from flask import jsonify, make_response


class BaseController:
	
	def __init__(self, request):
		self.request = request
		
	def user(self, *keys):
		return Auth.user(*keys)
		
	def request_params(self, *keys):
		_json = self.get_json()
		if keys:
			values = list()
			for key in keys:
				values.append(_json[key]) if key in _json else values.append(None)
			return values
		
		return _json
	
	def get_params(self, *keys):
		values = list()
		for key in keys:
			values.append(self.request.args.get(key))
		return values
	
	def get_json(self):
		return self.request.get_json()
	
	def handle_response(self, msg='OK', payload=None, status_code=200, slack_response=None):
		
		# If there is no specific slack formatted response, default to WEB API Response format
		if slack_response is None:
			data = {'msg': msg}
			if payload is not None:
				data['payload'] = payload
		else:
			data = slack_response
		
		response = jsonify(data)
		response.status_code = status_code
		return response
	
	def missing_required(self, params):
		return True if None in params or '' in params else False
	
	def missing_response(self, msg='Missing Required Parameters'):
		return self.handle_response(msg=msg, status_code=400)
