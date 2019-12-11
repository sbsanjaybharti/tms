import os
from flask import Flask, request, jsonify, current_app
from ..utility.celery_config import make_celery
from flask_sqlalchemy import SQLAlchemy
import datetime
from ..model.task import Task
from ..config import config_by_name

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config_by_name[os.getenv('FLASK_CONFIG') or 'development'])

db = SQLAlchemy()
db.init_app(app)

celery = make_celery(app)

@celery.task(name='celery.processTheTask')
def processTheTask(id):

   task_obj = Task.query.filter_by(id=id).first()
   task_obj.status = 400
   task_obj.resolved_at = datetime.datetime.now().strftime("%Y-%m-%d")
   task_obj.updated_at = datetime.datetime.now().strftime("%Y-%m-%d")
   task_obj.save()
   response_object = {
      'code': 200,
      'type': 'Success',
      'message': 'Task created successfully!',
   }
   return 'celerytasksanjay'



