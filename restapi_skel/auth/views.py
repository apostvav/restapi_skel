from flask import g, jsonify

from . import auth
from .. import authentication as login
from ..models import User


@auth.route('/token')
@login.login_required
def get_auth_token():
    token = g.user.generate_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@auth.route('/resource')
@login.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@login.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        # user = User.get_by_username(username_or_token)
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True
