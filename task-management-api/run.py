import os
import unittest
import operator
import eventlet
from threading import Lock

# from engineio.async_drivers import gevent
from flask import jsonify
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_migrate import Migrate, MigrateCommand
from flask_restplus import Api
from flask_script import Manager

from app import blueprint
from app.main import create_app, db
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from app.main.model import task, user
from app.main.model import blacklist
from app.main.service.TaskService import TaskService
import eventlet
eventlet.monkey_patch()
async_mode = None

app = create_app(os.getenv('FLASK_CONFIG') or 'development')
if os.getenv('DEBUG_MODE') == 'False':
    api = Api(app, ui=False, specs=False)


socketio = SocketIO(app, logger=True, engineio_logger=True, async_mode=async_mode)
thread = None
thread_lock = Lock()

app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'connected', 'status': 'connected'},
                      namespace='/test')

@app.route('/broadcast')
def broadcast():
    return render_template('broadcast.html', async_mode=socketio.async_mode)

@app.route('/broadcast/new')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/broadcast/update/<id>')
def update(id):
    return render_template('update.html', async_mode=socketio.async_mode, id=id)

@app.route('/broadcast/list')
def list():
    return render_template('list.html', async_mode=socketio.async_mode)

#
# @socketio.on('my_event', namespace='/test')
# def test_message(message):
#     print("------------------------------------------My event------------------------------------------" + message['data'])
#     # session['receive_count'] = session.get('receive_count', 0) + 1
#     if message['data'] != 'connected':
#         task = TaskService.get(message['data'])
#         print("------------------------------------------My task------------------------------------------" + str(task['code']))
#         if task['code'] == 200:
#             emit('my_response',
#                  {'data': task['data'], 'coming': 'event-sucess', 'status': task['code']})
#         else:
#             emit('my_response',
#                  {'data': task, 'coming': 'event-failed', 'status': task['code']})
#

@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    print("------------------------------------------My broadcast------------------------------------------" + message['data'])
    # session['receive_count'] = session.get('receive_count', 0) + 1
    task = TaskService.get(message['data'])
    if task['code'] == 200:
        emit('my_response',
             {'data': task['data'], 'status': task['code']},
             broadcast=True)
    else:
        emit('my_response',
             {'data': task, 'status': task['code']},
             broadcast=True)


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'connecting', 'status': 'connecting', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


@app.teardown_request
def session_clear(exception=None):
    # db.session.remove()
    # print("remove session")
    if exception and db.session.is_active:
        db.session.rollback()

@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@app.cli.command()
def routes():
    'Display registered routes'
    rules = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        rules.append((rule.endpoint, methods, str(rule)))

    sort_by_rule = operator.itemgetter(2)
    for endpoint, methods, rule in sorted(rules, key=sort_by_rule):
        route = '{:50s} {:25s} {}'.format(endpoint, methods, rule)
        print(route)

if __name__ == '__main__':
    # manager.run()
    socketio.run(app, debug=True)
