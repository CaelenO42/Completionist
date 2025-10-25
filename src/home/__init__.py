from flask import Blueprint

bp = Blueprint('home', __name__)

from src.home import routes