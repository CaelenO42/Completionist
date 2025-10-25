from dotenv import load_dotenv
import os

from flask import render_template, request, session, redirect, url_for
from src.user import account_bp, signin_bp

from google.oauth2 import id_token
from google.auth.transport import requests

from src.utils.db_user import db_user

load_dotenv()

@signin_bp.route('/', methods=('GET', 'POST'))
def signin():
  if request.method == 'POST':
    if 'credential' in request.form:
      try:
        idinfo = id_token.verify_oauth2_token(request.form['credential'], requests.Request(), os.getenv("GOOGLE_OAUTH_KEY"))

        google_sub = idinfo['sub']
        email = idinfo['email']
        name = idinfo['name']

        if db_user.exists_google_sub(google_sub):
          user = db_user.get_user_from_google_sub(google_sub)
          session['user'] = user

          return(redirect(url_for("home.index")))
        elif db_user.exists_email(email):
          db_user.link_google_sub(email, google_sub)
          
          user = db_user.get_user_from_google_sub(google_sub)
          session['user'] = user

          return(redirect(url_for("home.index")))
        else:
          db_user.insert_user(name, email, google_sub)

          user = db_user.get_user_from_google_sub(google_sub)
          session['user'] = user

          return(redirect(url_for("home.index")))
      except ValueError:
        return redirect(url_for("signin.signin"))
    return render_template('user/sign_in.html')
  else: return render_template('user/sign_in.html')

@account_bp.route('/signout')
def signout():
  if 'user' in session: del session['user']
  return redirect(url_for('home.index'))