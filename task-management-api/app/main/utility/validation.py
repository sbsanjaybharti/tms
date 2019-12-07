from flask import jsonify, Flask
import datetime
import re

# Error handler
class Validation():
    def createTask(data):
        error = []

        if data.get('title') is None or data.get('title') == '':
            error.append('Title is required')
        if data.get('description') is None or data.get('description') == '':
            error.append('Description is required')
        if data.get('due_date') is None or data.get('due_date') == '':
            error.append('Due date is required')
        else:
            try:
                datetime.datetime.strptime(data.get('due_date'), '%Y-%m-%d')
            except ValueError:
                error.append('Incorrect due data format, should be YYYY-MM-DD')

        if len(error) >= 1:
            response_object = {
                'code': 400,
                'type': 'Bad Request',
                'message': error
            }

            return response_object

    def UpdateTask(data):
        error = []

        if data.get('title') is None or data.get('title') == '':
            error.append('Title is required')
        if data.get('description') is None or data.get('description') == '':
            error.append('Description is required')
        if data.get('due_date') is None or data.get('due_date') == '':
            error.append('Due date is required')
        else:
            try:
                datetime.datetime.strptime(data.get('due_date'), '%Y-%m-%d')
            except ValueError:
                error.append('Incorrect due data format, should be YYYY-MM-DD')
        try:
            datetime.datetime.strptime(data.get('resolved_at'), '%Y-%m-%d')
        except ValueError:
            error.append('Incorrect due data format, should be YYYY-MM-DD')

        if len(error) >= 1:
            response_object = {
                'code': 400,
                'type': 'Bad Request',
                'message': error
            }

            return response_object
