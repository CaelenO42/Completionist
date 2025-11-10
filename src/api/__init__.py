from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
task_bp = Blueprint('task', __name__)

from src.api import routes