from flask_restplus import Namespace, fields


# USER Field
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
        'resolved_at': fields.Date(required=False, description='Resolved date is required'),
    })
    task_list = api.model('task_list', {
        'title': fields.String(required=True, description='Title is required'),
        'description': fields.String(required=True, description='Short description required'),
        'priority': fields.Integer(required=False, description=''),
        'status': fields.Integer(required=False, description=''),
        'due_date': fields.Date(required=True, description='Due date is required'),
    })