from flask import jsonify, request, abort, g

from . import tasks
from .. import authentication as login
from .. import db
from ..models import Task


@tasks.route('/<int:task_id>', methods=['GET'])
@login.login_required
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == g.user.id:
        return jsonify({'tasks': [task.serialize()]})
    else:
        abort(403)


@tasks.route('/', methods=['GET'])
@login.login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=g.user.id)
    return jsonify({'tasks': [task.serialize() for task in tasks]})


@tasks.route('/', methods=['POST'])
@login.login_required
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400)
    title = request.json['title']
    description = request.json['description']
    date = request.json['date']
    due_date = request.json['due_date']
    done = request.json['done']
    user_id = g.user.id
    task = Task(title, description, date, due_date, done, user_id)
    db.session.add(task)
    db.session.commit


@tasks.route('/<int:task_id>', methods=['PUT'])
@login.login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if not request.json:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task.title = request.json['title']
    task.description = request.json['description']
    task.date = request.json['date']
    task.due_date = request.json['due_date']
    task.done = request.json['done']
    task.user_id = request.json['user_id']
    db.session.commit()


@tasks.route('/<int:task_id>', methods=['DELETE'])
@login.login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
