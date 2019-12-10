import http.client
import os, json

import requests
from flask import request, session, jsonify, Flask
from flask_cors import cross_origin
from flask_restplus import Resource
from ..utility.ErrorHandler import responseData
from ..utility.validation import Validation
from ..service.TaskService import TaskService
from ..dto.dto import TaskDto

api = TaskDto.api
task_create = TaskDto.task_create
task_list = TaskDto.task_list
task_update = TaskDto.task_update

parser = api.parser()
parser.add_argument('Authorization', type=str, location='headers')

@api.route('/')
@api.header('Authorization: bearer', 'JWT TOKEN', required=True)
@api.doc(parser=parser)
class TaskController(Resource):
    """
    Create Task
    """
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @api.expect(task_create, validate=True)
    def post(self):

        """
         API to create task
         ## Implementation Notes
         __Access__ : Admin
        """
        patch_data = request.json
        validation = Validation.createTask(patch_data)

        if validation is not None:
            return responseData(validation)

        task = TaskService.create(patch_data)

        return responseData(task)

    # list user of current logged in user
    # user->organization-> list all user of that organization
    @cross_origin(headers=['Content-Type', 'Authorization'])
    # @api.doc(params={'page': 'Pagination no. of page'})
    @api.doc(params={'page': 'Pagination no. of page'})
    # @api.marshal_list_with(task_list, envelope='data')
    def get(self):
        """
         API to list task
         ## Implementation Notes
         __Access__ : Admin
        """
        # get user list
        args = request.args
        return responseData(TaskService.list(args))


@api.route('/<id>')
@api.header('Authorization: bearer', 'JWT TOKEN', required=True)
@api.doc(parser=parser)
class TaskViewController(Resource):
    @cross_origin(headers=['Content-Type', 'Authorization'])
    def get(self, id):
        """
         API to get the task
         ## Implementation Notes
         __Access__ : Admin
        """
        return responseData(TaskService.get(id))

    # Edit user detail(first name, last name, email)
    # return user data with auth0 id
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @api.expect(task_update, validate=True)
    def put(self, id):
        """
         API to update the task
         ## Implementation Notes
         __Access__ : Admin
        """
        patch_data = request.json
        validation = Validation.UpdateTask(patch_data)

        if validation is not None:
            return responseData(validation)

        return responseData(TaskService.edit(patch_data, id))
#
# @api.route('/<id>')
# @api.header('Authorization: bearer', 'JWT TOKEN', required=True)
# @api.doc(parser=parser)
# class TaskReminderController(Resource):
#     @cross_origin(headers=['Content-Type', 'Authorization'])
#     def get(self, id):
#         """
#          API to get the user
#          ## Implementation Notes
#          __Access__ : Admin
#         """
#         return responseData(TaskService.reminder(id))
