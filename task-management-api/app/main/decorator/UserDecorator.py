import json
import os

from six.moves.urllib.request import urlopen
from functools import wraps

from flask import Flask, request, jsonify, _request_ctx_stack
from flask_cors import cross_origin
from jose import jwt

from app.main.model.user import User
from app.main import current_user
from ..utility.ErrorHandler import AuthError, responseData, getException


# Format error response and append status code

def isAdmin(func):
    @wraps(func)
    def decorated(*args, **kwargs):

        try:
            user = current_user()
            id = user.is_admin
            if user.is_admin == True:
                return func(*args, **kwargs)
            else:
                response_object = {
                    'code': 401,
                    'type': 'Unauthorized',
                    'message': 'You are not allowed to view this page!'
                }
                return responseData(response_object)
        except Exception:

            response_object = {
                'code': 404,
                'type': 'Not Found',
                'message': 'Page does not exist!',
                'exception': getException()
            }
            return responseData(response_object)

    return decorated