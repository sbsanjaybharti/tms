from flask_restplus import Api
from flask import Blueprint
from .main.controller.TaskController import api as task
from .main.controller.AuthController import api as auth
from .main.controller.UserController import api as user

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Omnius Backend challenge',
          version='0.0.1',
          description='Simple task management system for backend challenge'
          )

api.add_namespace(auth, path='/v1/auth')
api.add_namespace(user, path='/v1/user')
api.add_namespace(task, path='/v1/task')