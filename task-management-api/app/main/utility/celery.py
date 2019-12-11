import os
from flask import Flask, request, jsonify, current_app
from ..utility.celery_config import make_celery
from flask_sqlalchemy import SQLAlchemy
import datetime
from ..model.task import Task
from ..config import config_by_name
import uuid

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
   return 'Task move to process successfully!'


@celery.task(name='celery.task.add')
def taskCreate(data, id):

   if data.get('priority') is None or data.get('priority') == '' or data.get('priority') == 0:
      priority = 100
   else:
      priority = data.get('priority')
   new_task = Task(
      id=id,
      title=data.get('title'),
      description=data.get('description'),
      priority=priority,
      status=100,
      due_date=data.get('due_date'),
   )
   new_task.save()

   return 'Task created successfully!'


@celery.task(name='celery.task.update')
def taskUpdate(data, id):

   if data.get('priority') is None or data.get('priority') == '' or data.get('priority') == 0:
      priority = 100
   else:
      priority = data.get('priority')
   if data.get('status') is None or data.get('status') == '' or data.get('status') == 0:
      status = 100
   else:
      status = data.get('status')
   task_obj = Task.query.filter_by(id=id).first()

   task_obj.title = data.get('title')
   task_obj.description = data.get('description')
   task_obj.priority = priority
   task_obj.status = status
   task_obj.due_date = data.get('due_date')
   task_obj.resolved_at = data.get('resolved_at')
   task_obj.remind_me_at = data.get('remind_me_at')
   task_obj.updated_at = datetime.datetime.now().strftime("%Y-%m-%d")
   task_obj.save()

   return 'Task updated successfully!'


