from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from src.api import routes