from dotenv import load_dotenv
import os

from flask import render_template, request, session, redirect, url_for, jsonify
from src.user import account_bp, signin_bp

from google.oauth2 import id_token
from google.auth.transport import requests

from src.utils.db_user import db_user
from src.utils.JWTGenerator import JWTGen
from src.utils.MailSender import MailSender
from src.api.routes import _issue_new_tokens_and_cookies, _remove_tokens_and_cookies

from time import sleep

from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies

load_dotenv()

@signin_bp.route('/', methods=('GET', 'POST'))
def signin():
  if request.method == 'POST':
    if 'credential' in request.form:
      try:
        sleep(0.001) # Fix weird clock sync bug
        idinfo = id_token.verify_oauth2_token(request.form['credential'], requests.Request(), os.getenv("GOOGLE_OAUTH_KEY"))

        google_sub = idinfo['sub']
        email = idinfo['email'].lower()

        if db_user.exists_email(email) and not db_user.exists_google_sub(google_sub): db_user.link_google_sub(email, google_sub)
        elif not db_user.exists_google_sub(google_sub):
          session['email'] = email
          session['google_sub'] = google_sub

          return(redirect(url_for("account.onboarding")))
        
        user = db_user.get_user_from_google_sub(google_sub)
        session['user'] = user

        # refresh_token = create_refresh_token(identity=user["uuid"])
        # access_token = create_access_token(identity=user["uuid"])

        # response = redirect(url_for("dashboard.index"))
        # set_access_cookies(response, access_token)
        # set_refresh_cookies(response, refresh_token)

        return _issue_new_tokens_and_cookies(user["uuid"])
      except ValueError:
        print("error!")
        return redirect(url_for("signin.signin"))
    
    if not request.form["email"]: return render_template('user/sign_in.html', invalid_email=True) 
    email = request.form["email"].lower()
    jwt = None
    if db_user.exists_email(email):
      uuid = db_user.get_uuid_by_email(email)
      jwt = JWTGen.encode_jwt(email, uuid)
    else: jwt = JWTGen.encode_jwt(email)

    print(f"https://localhost/account/verify/{jwt}")
    # exists_mail = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    # if exists_mail: MailSender.verification_email(email, jwt)
    # else: print(f"http://localhost:5000/account/verify/{jwt}")
    return render_template('user/sign_in.html', magic_link=True) 

  else: 
    if 'email' in session: return redirect(url_for("account.onboarding"))
    google_oauth = os.getenv("GOOGLE_OAUTH_KEY")
    return render_template('user/sign_in.html', google_oauth=google_oauth)

@account_bp.route('/signout')
def signout():
  if 'user' in session: 
    session.pop('user', None)
    return _remove_tokens_and_cookies(request)
  else: return redirect(url_for('home.index'))

@account_bp.route('/verify/<jwt>')
def verify(jwt):
  if not jwt: return redirect(url_for('signin.signin', invalid_link=True))
  claims = JWTGen.decode_jwt(jwt)
  if not claims: return redirect(url_for('signin.signin', invalid_link=True))
  if 'uuid' in claims:
    user = db_user.get_user_from_uuid(claims['uuid'])
    session['user'] = user

    # refresh_token = create_refresh_token(identity=user["uuid"])
    # access_token = create_access_token(identity=user["uuid"])

    # response = redirect(url_for("dashboard.index"))
    # set_access_cookies(response, access_token)
    # set_refresh_cookies(response, refresh_token)

    return _issue_new_tokens_and_cookies(user["uuid"])
  elif 'email' in claims:
    session['email'] = claims['email']
    return redirect(url_for("account.onboarding"))
  
@account_bp.route('/onboarding', methods=('GET', 'POST'))
def onboarding():
  if request.method == 'POST':
    if 'cancel' in request.form:
      del session['email']
      del session['google_sub']
      return redirect(url_for("home.index"))
    if 'email' not in session: return redirect(url_for('home.index'))
    if 'username' in request.form and len(request.form['username']) >= 1:
      email = session['email']
      del session['email']
      db_user.insert_user(request.form['username'][:20], email, session.get('google_sub', None))
      del session['google_sub']

      user = db_user.get_user_from_email(email)
      session['user'] = user

      # refresh_token = create_refresh_token(identity=user["uuid"])
      # access_token = create_access_token(identity=user["uuid"])

      # response = redirect(url_for("dashboard.index"))
      # set_access_cookies(response, access_token)
      # set_refresh_cookies(response, refresh_token)

      return _issue_new_tokens_and_cookies(user["uuid"])
    else: return render_template('user/onboarding.html', invalid_username = True)
  else:
    if 'email' in session: return render_template('user/onboarding.html')
    else: return redirect(url_for('home.index'))

