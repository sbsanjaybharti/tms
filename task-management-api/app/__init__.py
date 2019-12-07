from flask_restplus import Api
from flask import Blueprint
from .main.controller.TaskController import api as task

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Omnius Backend challenge',
          version='0.0.1',
          description='Simple task management system for backend challenge'
          )

api.add_namespace(task, path='/v1/task')