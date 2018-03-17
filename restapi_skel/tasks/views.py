from flask import jsonify, request, abort, g

from . import tasks
from .. import authentication as login
from .. import db
from ..models import Task


@tasks.route('/<int:task_id>', methods=['GET'])
@login.login_required
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != g.user.id:
        abort(403)
    return jsonify({'tasks': [task.serialize()]})


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
    description = request.json.get('description', "")
    date = request.json.get('date', None)
    due_date = request.json.get('due_date', None)
    done = False
    user_id = g.user.id
    task = Task(title=title, description=description, date=date,
                due_date=due_date, done=done, user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return jsonify({'task': [task.serialize()]}), 201


@tasks.route('/<int:task_id>', methods=['PUT'])
@login.login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != g.user.id:
        abort(403)
    if not request.json:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task.title = request.json.get('title', task.title)
    task.description = request.json.get('description', task.description)
    task.date = request.json.get('date', task.date)
    task.due_date = request.json.get('due_date', task.due_date)
    task.done = request.json.get('done', task.done)
    db.session.commit()
    return jsonify({'task': [task.serialize()]})


@tasks.route('/<int:task_id>', methods=['DELETE'])
@login.login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != g.user.id:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'result': True})
