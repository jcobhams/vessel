from functools import wraps
from datetime import datetime
from flask import request, make_response, jsonify

class Security:
    
    @staticmethod
    def validator(rules):
        """
        :rules: list -  The sets of keys and rules to be applied
        example: [username|required:max-255:min-120, email|required:email]
        """
        
        def real_validate_request(f):
            
            @wraps(f)
            def decorated(*args, **kwargs):
                if not request.json:
                    return make_response(jsonify({'msg':'Bad Request - Request Must be JSON Formatted'})), 400
                
                payload = request.get_json()
                
                if payload:
                    #Loop through all validation rules
                    for rule in rules:
                        rule_array = rule.split('|')
                        
                        request_key = rule_array[0]
                        validators = rule_array[1].split(':')
                            
                        # If the key is not in the request payload, and required is not part of the validator rules,
                        # Continue the loop to avoid key errors.
                        if request_key not in payload and 'required' not in validators:
                            continue
                        
                        #Loop all validators specified in the current rule
                        for validator in validators:
                            
                            if validator == 'int' and type(payload[request_key]) is str and not payload[request_key].isdigit():
                                return make_response(jsonify({'msg': 'Bad Request - {} must be integer'.format(request_key)})), 400
                            
                            if validator == 'float':
                                try:
                                    float(payload[request_key])
                                except Exception as e:
                                    return make_response(jsonify({'msg': 'Bad Request - {} must be float'.format(request_key)})), 400
                            
                            if (validator == 'required' and request_key not in payload) or payload[request_key] == '':
                                return make_response(jsonify({'msg': 'Bad Request - {} is required'.format(request_key)})), 400
                            
                            if validator.find('max') > -1:
                                max_value = int(validator.split('-')[1])
                                if int(payload[request_key]) > max_value:
                                    return make_response(jsonify({'msg': 'Bad Request - {} can only have a max value of {}'.format(request_key, max_value)})), 400
                            
                            if validator.find('min') > -1:
                                min_value = int(validator.split('-')[1])
                                if int(payload[request_key]) < min_value:
                                    return make_response(jsonify({'msg': 'Bad Request - {} can only have a min value of {}'.format(request_key, min_value)})), 400
                            
                            if validator.find('length') > -1:
                                length_value = int(validator.split('-')[1])
                                if len(str(payload[request_key])) > length_value:
                                    return make_response(jsonify({'msg': 'Bad Request - {} can only have a len of {}'.format(request_key, length_value)})), 400
                                
                            if validator == 'exists':
                                import importlib
                                from app.utils import to_pascal_case
                                
                                repo_name = rule_array[2]
                                column_name = rule_array[3]
                                
                                rep = 'app.repositories.{}_repo'.format(repo_name)
                                mod = importlib.import_module(rep)
                                repo_class = getattr(mod, '{}Repo'.format(to_pascal_case(repo_name)))
                                repo = repo_class()
                                
                                if type(payload[request_key]) == int:
                                    v = repo.find_first(**{column_name: payload[request_key]})
                                        
                                    if not v:
                                        return make_response(jsonify({'msg': 'Bad Request - {} contains invalid {}(s) for {} table '.format(request_key, column_name, repo_name)})), 400

                                if type(payload[request_key]) == list:
                                    for val in payload[request_key]:
                                        v = repo.find_first(**{column_name:val})
                                        
                                        if not v:
                                            return make_response(jsonify({'msg': 'Bad Request - {} contains invalid {}(s) for {} table '.format(request_key, column_name, repo_name)})), 400

                            if validator == 'date':
                                try:
                                    datetime.strptime(payload[request_key], '%Y-%m-%d')
                                except Exception as e:
                                    return make_response(jsonify({'msg': 'Bad Request - {} should be valid date. Format: YYYY-MM-DD'.format(request_key)})), 400

                            if validator == 'list' and type(payload[request_key]) is not list:
                                return make_response(jsonify({'msg': 'Bad Request - {} must be a list'.format(request_key)})), 400\

                            if validator == 'list_int':
                                if type(payload[request_key]) is not list:
                                    return make_response(jsonify({'msg': 'Bad Request - {} must be a list'.format(request_key)})), 400
                                for val in payload[request_key]:
                                    if type(val) is not int:
                                        return make_response(jsonify({'msg': 'Bad Request - [{}] in list must be integer'.format(val)})), 400

                return f(*args, **kwargs)
            
            return decorated
        
        return real_validate_request