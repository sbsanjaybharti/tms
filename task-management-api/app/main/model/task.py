from .. import db, flask_bcrypt
import uuid
import datetime


# Define the UserRoles association table
class Task(db.Model):
    __tablename__ = 'tasks'

    priority_disc = {
            100: 'Low',
            200: 'Medium',
            300: 'High',
        }
    status_disc = {
            100: 'Created',
            200: 'Pending',
            300: 'Started',
            400: 'Completed',
            500: 'Close',
        }

    # id = db.Column(db.Integer(), primary_key=True)
    id = db.Column(db.String(100), primary_key=True, autoincrement=False, unique=True, default=str(uuid.uuid4()))
    title = db.Column(db.String(100), index=True)
    description = db.Column(db.Text(), index=True)
    priority = db.Column(db.Integer())  # 100 Low, 200 Medium, 300 High
    status = db.Column(db.Integer())  # 100 created, 200 pending, 300 started, 400 completed, 500 close

    due_date = db.Column(db.DateTime, nullable=True)
    resolved_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def getPriority(self):
        return self.priority_disc[self.priority]

    def getStatus(self):
        return self.priority_disc[self.status]

