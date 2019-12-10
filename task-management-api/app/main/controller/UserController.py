from flask import request
from flask_restplus import Resource

from ..dto.dto import UserDto
from ..service.UserService import UserService
from ..utility.ErrorHandler import responseData

api = UserDto.api
user_create = UserDto.user_create


@api.route('/')
class UserList(Resource):

    @api.doc('create a new user')
    @api.expect(user_create, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        result = UserService.create(data=data)
        return responseData(result)
