from src.api import auth_bp, task_bp

from flask import render_template, request, session, redirect, url_for, make_response, jsonify, Request
from flask_jwt_extended import jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies, unset_jwt_cookies, create_access_token, create_refresh_token, get_jwt, get_jti, decode_token 

from src.utils.db_task import db_task

import redis

from src import JWTManager

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
  refresh_payload = get_jwt()
  current_refresh_jti = refresh_payload["jti"]
  current_user_identity = get_jwt_identity()

  redis_key = f"refresh_jti:{current_refresh_jti}"
  redis_conn = redis.Redis(host='localhost', port=6379, db=0)
  deleted_count = redis_conn.delete(redis_key)

  if deleted_count == 0: return jsonify({"msg": "Invalid or already used refresh token."}), 401

  return _issue_new_tokens_and_cookies(current_user_identity, True)


@task_bp.route('/set', methods=['POST'])
@jwt_required()
def set_task():
  current_user = get_jwt_identity()
  return(jsonify({"msg": "Request successful"}), 200)

@task_bp.route('/get', methods=['POST'], defaults={'taskId': None})
@task_bp.route('/get/<taskId>', methods=['POST'])
@jwt_required()
def get_task(taskId):
  identity = get_jwt_identity()
  if not taskId:
    tasks = db_task.get_tasks(identity)
    print(tasks)
    return (jsonify(tasks), 200)

  
def _issue_new_tokens_and_cookies(identity, refresh=False):
  new_access_token = create_access_token(identity=identity)
  new_refresh_token = create_refresh_token(identity=identity)

  new_refresh_jti = get_jti(new_refresh_token)

  redis_conn = redis.Redis(host='localhost', port=6379, db=0)
  # Set the JTI to auto expire in 30 days
  JTI_EXPIRY_SECONDS = 2592000
  redis_conn.set(f"refresh_jti:{new_refresh_jti}", identity, ex=JTI_EXPIRY_SECONDS)

  if refresh:
    response = make_response(jsonify({
      "msg": f'Token refreshed for {identity}'
    }), 200)
  else:
    response = redirect(url_for("dashboard.index"))

  set_access_cookies(response, new_access_token)
  set_refresh_cookies(response, new_refresh_token)

  return response

def _remove_tokens_and_cookies(request: Request):
  try:
    refresh_token = request.cookies.get('refresh_token_cookie')
    if refresh_token:
      refresh_payload = decode_token(refresh_token)
      current_refresh_jti = refresh_payload["jti"]

      redis_key = f"refresh_jti:{current_refresh_jti}"
      redis_conn = redis.Redis(host='localhost', port=6379, db=0)
      redis_conn.delete(redis_key)
  except Exception as e:
    print(f'Warning: Could not decode refresh token for cleanup: {e}')
    pass

  response = redirect(url_for("home.index"))
  unset_jwt_cookies(response)
  return response