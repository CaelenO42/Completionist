from flask import Flask, render_template
from flask_session import Session

from config import Config

def bad_request(e):
  return render_template('error/400.html', e=e), 400

def page_not_found(e):
  return render_template('error/404.html', e=e), 404

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)

  server_session = Session(app)

  # Register Pages for 400 and 404 errors
  app.register_error_handler(400, bad_request)
  app.register_error_handler(404, page_not_found)

  # Home blueprint
  from src.home import bp as home_bp
  app.register_blueprint(home_bp)

  return app