from flask import Blueprint

tasks = Blueprint('tasks', __name__)

from .views import *
