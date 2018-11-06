import jwt
from functools import wraps
from flask import request, jsonify, make_response
# from app.repositories.permission_repo import PermissionRepo
# from app.repositories.user_role_repo import UserRoleRepo

class Auth:
	''' This class will house Authentication and Authorization Methods '''
	
	''' Routes The Location Header Should Not Be Applied To'''
	location_header_ignore = [
		'/locations'
	]
	
	''' Routes The Authentication Header Should Not Be Applied To'''
	authentication_header_ignore = [
		'/',
		'/docs'
	]
	
	@staticmethod
	def check_token():
		if request.method != 'OPTIONS':
			
			# if '/' in Auth.authentication_header_ignore:
			# 	return None
			#
			for endpoint in Auth.authentication_header_ignore:
				if request.path.find(endpoint) > -1: # If endpoint in request.path, ignore this check
					return None

			try:
				token = Auth.get_token()
			except Exception as e:
				print(e)
				return make_response(jsonify({'msg': str(e)}),400)

			try:
				decoded = Auth.decode_token(token)
			except Exception as e:
				return make_response(jsonify({'msg': str(e)}), 400)
	
	@staticmethod
	def _get_user():
		token = None
		try:
			token = Auth.get_token()
		except Exception as e:
			raise e
		
		try:
			if token:
				return Auth.decode_token(token)['UserInfo']
		except Exception as e:
			raise e
	
	@staticmethod
	def user(*keys):
		user = Auth._get_user()
		if keys:
			if len(keys) > 1:
				values = list()
				for key in keys:
					values.append(user[key]) if key in user else values.append(None)
				return values
			if len(keys) == 1 and keys[0] in user:
				return user[keys[0]]
		
		return user
	
	@staticmethod
	def get_token(request_obj=None):
		if request_obj:
			header = request_obj.headers.get('Authorization', None)
		else:
			header = request.headers.get('Authorization', None)
		if not header:
			raise Exception('Authorization Header is Expected')
		
		header_parts = header.split()
		
		if header_parts[0].lower() != 'bearer':
			raise Exception('Authorization Header Must Start With Bearer')
		elif len(header_parts) > 1:
			return header_parts[1]
		
		raise Exception('Internal Application Error')
	
	@staticmethod
	def decode_token(token, jwtsecret=''):
		try:
			decoded = jwt.decode(token, jwtsecret, verify=False)
			return decoded
		except jwt.ExpiredSignature:
			raise Exception('Token is Expired')
		except jwt.DecodeError:
			raise Exception('Error Decoding')
		
	@staticmethod
	def check_location_header():
		if request.method != 'OPTIONS':
			for endpoint in Auth.location_header_ignore:
				if request.path.find(endpoint) > -1: # If endpoint in request.path, ignore this check
					return None
			try:
				Auth.get_location()
			except Exception as e:
				return make_response(jsonify({'msg': str(e)}), 400)
		
	@staticmethod
	def get_location():
		location = request.headers.get('X-Location', None)
		if not location:
			raise Exception('Location Header is Expected')
		if not location.isdigit():
			raise Exception('Location Header Value is Invalid')
		return int(location)
	
	@staticmethod
	def has_permission(permission):
		
		def permission_checker(f):
			
			@wraps(f)
			def decorated(*args, **kwargs):
				user_role_repo = None #UserRoleRepo()
				permission_repo = None #PermissionRepo()
				
				user_id = Auth.user('id')
				user_role = user_role_repo.find_first(**{'user_id': user_id})
				
				if not user_id:
					return make_response(jsonify({'msg': 'Missing User ID in token'})), 400

				if not user_role:
					return make_response(jsonify({'msg': 'Access Error - No Role Granted'})), 400

				user_perms = permission_repo.filter_by(**{'role_id': user_role.role_id})
				
				perms = [perm.keyword for perm in user_perms.items]
				if len(perms) == 0:
						return make_response(jsonify({'msg': 'Access Error - No Permission Granted'})), 400
				
				if permission not in perms:
					return make_response(jsonify({'msg': 'Access Error - Permission Denied'})), 400
				
				return f(*args, **kwargs)
			
			return decorated
		return permission_checker
	
		