from flask import jsonify, abort

from . import main
# from ..models import User


@main.route('')
@main.route('index')
def index():
    return jsonify({'Hello': 'World'})


@main.route('test')
def test():
    abort(400)


@main.route('test2')
def test2():
    return jsonify({'message': 'YOLO'})


@main.app_errorhandler(400)
def bad_request_error(e):
    return jsonify({'message': 'Bad Request'}), 400


@main.app_errorhandler(403)
def forbidden_error(e):
    return jsonify({'message': 'Forbidden'}), 403


@main.app_errorhandler(404)
def not_found_error(e):
    return jsonify({'message': 'Not Found'}), 404


@main.app_errorhandler(500)
def server_error(e):
    return jsonify({'message': 'Server Error'}), 500
