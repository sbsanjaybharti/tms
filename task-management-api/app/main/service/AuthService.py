from ..model.user import User
from ..service.BlacklistService import save_token
from ..utility.ErrorHandler import getException


class Auth:

    @staticmethod
    def login_user(data):
        try:
            # fetch the user data
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    response_object = {
                        'code': 200,
                        'type': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token.decode()
                    }
                    return response_object
            else:
                response_object = {
                    'code': 403,
                    'type': 'fail',
                    'message': 'email or password does not match.'
                }
                return response_object

        except Exception as e:
            response_object = {
                'code': 500,
                'type': 'Internal Server Errors',
                'message': 'Exception occur in task service, Try again later!',
                'exception': getException()
            }
            return response_object

    @staticmethod
    def logout_user(data):
        # if data:
        #     auth_token = data.split(" ")[1]
        # else:
        #     auth_token = ''

        auth_token = data
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                return save_token(token=auth_token)
            else:
                response_object = {
                    'code': 403,
                    'type': 'fail',
                    'message': resp
                }
                return response_object
        else:
            response_object = {
                'code': 403,
                'type': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object

    @staticmethod
    def get_logged_in_user(new_request):
            # get the auth token
            auth_token = new_request.headers.get('Authorization')
            if auth_token:
                resp = User.decode_auth_token(auth_token)
                if not isinstance(resp, str):
                    user = User.query.filter_by(id=resp).first()
                    response_object = {
                        'code': 200,
                        'status': 'success',
                        'data': {
                            'user_id': user.id,
                            'email': user.email,
                            'admin': user.admin,
                            'registered_on': str(user.registered_on)
                        }
                    }
                    return response_object, 200
                response_object = {
                    'code': 401,
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
            else:
                response_object = {
                    'code': 401,
                    'status': 'fail',
                    'message': 'Provide a valid auth token.'
                }
                return response_object, 401
