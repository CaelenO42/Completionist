from flask import Flask, render_template
from flask_session import Session
from flask_jwt_extended import JWTManager

from config import Config

def bad_request(e):
  return render_template('error/400.html', e=e), 400

def page_not_found(e):
  return render_template('error/404.html', e=e), 404

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)

  server_session = Session(app)
  jwt = JWTManager(app)

  # Register Pages for 400 and 404 errors
  app.register_error_handler(400, bad_request)
  app.register_error_handler(404, page_not_found)

  # Home blueprint
  from src.home import bp as home_bp
  app.register_blueprint(home_bp)

  # Dashboard blueprint
  from src.dashboard import bp as dashboard_bp
  app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

  # User blueprint
  from src.user import account_bp
  from src.user import signin_bp

  app.register_blueprint(account_bp, url_prefix='/account')
  app.register_blueprint(signin_bp, url_prefix='/signin')

  # API blueprint
  from src.api import auth_bp
  from src.api import task_bp
  from src.api import category_bp
  app.register_blueprint(auth_bp, url_prefix='/api/auth')
  app.register_blueprint(task_bp, url_prefix='/api/task')
  app.register_blueprint(category_bp, url_prefix='/api/category')

  return app