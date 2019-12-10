import datetime

from app.main import db
from ..utility.ErrorHandler import getException
from ..model.user import User


class UserService:
    def create(data):
        try:
            user = User.query.filter_by(email=data['email']).first()
            if not user:
                new_user = User(
                    email=data['email'],
                    username=data['email'],
                    password=data['password'],
                    registered_on=datetime.datetime.utcnow()
                )
                new_user.save()

                response_object = {
                    'code': 200,
                    'type': 'Success',
                    'message': 'Successfully registered!',
                }
                return response_object
            else:
                response_object = {
                    'code': 409,
                    'type': 'fail',
                    'message': 'User already exists. Please Log in.',
                }
                return response_object
        except Exception as e:
            response_object = {
                'code': 500,
                'type': 'Internal Server Errors',
                'message': 'Exception occur in task service, Try again later!'
            }
            return response_object

    def generate_token(user):
        try:
            # generate the auth token
            auth_token = user.encode_auth_token(user.id)
            response_object = {
                'code': 200,
                'type': 'Success',
                'message': 'Successfully registered!',
                'Authorization': auth_token.decode()
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
