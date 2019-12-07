import os
import unittest
import operator
from threading import Lock

from flask import jsonify
from flask import Flask, render_template
from flask_migrate import Migrate, MigrateCommand
from flask_restplus import Api
from flask_script import Manager

from app import blueprint
from app.main import create_app, db
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from app.main.model import task
async_mode = None

app = create_app(os.getenv('FLASK_CONFIG') or 'development')
if os.getenv('DEBUG_MODE') == 'False':
    api = Api(app, ui=False, specs=False)


socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@app.route('/broadcast')
def broadcast():
    return render_template('broadcast.html', async_mode=socketio.async_mode)

@app.route('/broadcast/new')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/broadcast/list')
def list():
    return render_template('list.html', async_mode=socketio.async_mode)


@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    emit('my_response',
         {'data': 'you are here', 'count': 1},
         broadcast=True)

@app.teardown_request
def session_clear(exception=None):
    db.session.remove()
    print("remove session")
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
    manager.run()
