from flask_restplus import Namespace, fields


# USER Field
class UserDto:
    api = Namespace('User Service', description='User details')

    user_create = api.model('user_create', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
    })
    
class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

# Task Field
class TaskDto:
    api = Namespace('Task Service', description='Task details')

    task_create = api.model('task_create', {
        'title': fields.String(required=True, description='Title is required'),
        'description': fields.String(required=True, description='Short description required'),
        'priority': fields.Integer(required=False, description='(Optional) by default it will be low'),
        'due_date': fields.Date(required=True, description='Due date is required'),
    })
    task_update = api.model('task_update', {
        'title': fields.String(required=True, description='Title is required'),
        'description': fields.String(required=True, description='Short description required'),
        'priority': fields.Integer(required=False, description='(Optional) by default it will be low'),
        'status': fields.Integer(required=False, description='Optional'),
        'due_date': fields.Date(required=True, description='Due date is required'),
        'resolved_at': fields.Date(required=False, description='Resolved date is optional'),
        'remind_me_at': fields.Date(required=False, description='Remind me date is optional'),
    })
    task_list = api.model('task_list', {
        'title': fields.String(required=True, description='Title is required'),
        'description': fields.String(required=True, description='Short description required'),
        'priority': fields.Integer(required=False, description=''),
        'status': fields.Integer(required=False, description=''),
        'due_date': fields.Date(required=True, description='Due date is required'),
    })