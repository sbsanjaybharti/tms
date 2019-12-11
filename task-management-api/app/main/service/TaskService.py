import os, json
import re
import secrets
import uuid

from ..model.task import Task
from ..utility.ErrorHandler import getException
from sqlalchemy import asc, desc, and_
from flask import Flask, request, jsonify, current_app
from ..utility.celery import processTheTask

import datetime



class TaskService:
    @staticmethod
    def create(data):
        try:
            if data.get('priority') is None or data.get('priority') == '' or data.get('priority') == 0:
                priority = 100
            else:
                priority = data.get('priority')

            new_task = Task(
                    id=str(uuid.uuid4()),
                    title=data.get('title'),
                    description=data.get('description'),
                    priority=priority,
                    status=100,
                    due_date=data.get('due_date'),
            )
            new_task.save()

            response_object = {
                'code': 200,
                'type': 'Success',
                'message': 'Task created successfully!',
                'data': {
                    'id': new_task.id,
                    'title': new_task.title,
                    'priority': new_task.priority,
                    'status': new_task.status,
                    'due_date': new_task.due_date,
                }
            }
            return response_object

        except Exception as e:
            response_object = {
                    'code': 500,
                    'type': 'Internal Server Errors',
                    'message': 'Exception occur in task service, Try again later!',
                    'exception': getException()
            }
            return response_object

    def list(args):
        try:

            if 'page' in args and args['page'] is not None:
                page = args['page']
            else:
                page = 1
            # order_by = 'due_date'

            task_list = Task.query.filter(Task.status != 400).order_by(desc('due_date, priority'))\
                .paginate(int(page), per_page=current_app.config['DATA_PERPAGE'])

            if task_list:
                result = [
                    {
                        'id': task.id,
                        'title': task.title,
                        'priority': task.getPriority(),
                        'due_date': task.getDueDate(),
                        'remind_me_at': task.getRemindMeAt(),
                        'status': task.getStatus()
                    } for task in task_list.items]

                response_object = {
                    'code': 200,
                    'type': 'Success',
                    'message': 'Task found',
                    'data': result,
                    'paginate': {
                        'pages': task_list.pages,
                        'page': task_list.page,
                        'per_page': task_list.per_page,
                        'total': task_list.total,
                        'prev_num': task_list.prev_num,
                        'next_num': task_list.next_num,
                        'has_prev': task_list.has_prev,
                        'has_next': task_list.has_next
                    }
                }
                return response_object
            else:
                response_object = {
                    'code': 404,
                    'type': 'Not Found',
                    'message': 'Task Not Found!'
                }
                return response_object

        except Exception as e:
            response_object = {
                    'code': 500,
                    'type': 'Internal Server Errors',
                    'message': 'Exception occur in task service, Try again later!',
                    'exception': getException()
            }
            return response_object


    @staticmethod
    def get(id):

        if not id:
            response_object = {
                'code': 404,
                'type': 'Not Found',
                'message': 'Page does not exist!'
            }
            return response_object
        try:

            task_obj = Task.query.filter_by(id=id).first()
            if not task_obj:
                response_object = {
                    'code': 400,
                    'type': 'Bad Response',
                    'message': 'Task does not exist!'
                }
                return response_object
            else:
                response_object = {
                    'code': 200,
                    'type': 'Success',
                    'message': 'Data found successfully!',
                    'data' : {
                        'id': task_obj.id,
                        'title': task_obj.title,
                        'description': task_obj.description,
                        'priority': task_obj.getPriority(),
                        'status': task_obj.getStatus(),
                        'due_date': task_obj.getDueDate(),
                        'resolved_at': task_obj.getResolvedAt(),
                        'remind_me_at': task_obj.getRemindMeAt(),
                        'created_at': task_obj.getCreatedAt(),
                        'updated_at': task_obj.getUpdatedAt()
                    }
                }
                return response_object

        except Exception as e:
            response_object = {
                    'code': 500,
                    'type': 'Internal Server Error',
                    'message': 'Exception occur in task service, Try again later!',
                    'exception': getException()
            }
            return response_object

    @staticmethod
    def process(id):

        if not id:
            response_object = {
                'code': 404,
                'type': 'Not Found',
                'message': 'Page does not exist!'
            }
            return response_object
        try:
            # ********************************************
            # Celery call for process the task
            # ********************************************

            task_obj = Task.query.filter_by(id=id).first()
            if task_obj.getRemindMeAt() is None:
                processTheTask.delay(id)
            else:
                processTheTask.s(id).apply_async(eta=task_obj.remind_me_at)
            # ********************************************
            # Celery call for process the task
            # ********************************************

            response_object = {
                'code': 200,
                'type': 'Success',
                'message': task_obj.getRemindMeAt(),
            }
            return response_object


        except Exception as e:
            response_object = {
                    'code': 500,
                    'type': 'Internal Server Error',
                    'message': 'Exception occur in task service, Try again later!',
                    'exception': 'Task added to process queue successfully '
            }
            return response_object

    @staticmethod
    def edit(data, id):
        try:
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

            response_object = {
                'code': 200,
                'type': 'Success',
                'message': 'Task updated successfully!',
                'data': {
                    'id': task_obj.id,
                    'title': task_obj.title,
                    'priority': task_obj.priority,
                    'status': task_obj.status,
                    'due_date': task_obj.due_date,
                }
            }
            return response_object

        except Exception as e:
            response_object = {
                    'code': 500,
                    'type': 'Internal Server Errors',
                    'message': 'Exception occur in task service, Try again later!',
                    'exception': getException()
            }
            return response_object


    @staticmethod
    def reminder(id):
        try:
            task_obj = Task.query.filter_by(id=id).first()

            response_object = {
                'code': 200,
                'type': 'Success',
                'message': 'Reminder send successfully!',
                'data': {
                    'date': task_obj.id,
                    'title': task_obj.title,
                }
            }
            return response_object

        except Exception as e:
            response_object = {
                    'code': 500,
                    'type': 'Internal Server Errors',
                    'message': 'Exception occur in reminder service, Try again later!',
                    'exception': getException()
            }
            return response_object
