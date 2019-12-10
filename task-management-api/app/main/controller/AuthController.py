from flask import request
from flask_restplus import Resource

from ..service.AuthService import Auth
from ..utility.ErrorHandler import responseData
from ..decorator.AuthDecorator import token_required
from ..dto.dto import AuthDto

api = AuthDto.api
user_auth = AuthDto.user_auth

parser = api.parser()
parser.add_argument('Authorization', type=str, location='headers')

@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return responseData(Auth.login_user(data=post_data))


@api.route('/logout')
@api.doc(parser=parser)
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    @token_required
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        return responseData(Auth.logout_user(data=auth_header))