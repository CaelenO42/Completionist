from dotenv import load_dotenv
import os

from flask import render_template, request, session, redirect, url_for
from src.user import account_bp, signin_bp

from google.oauth2 import id_token
from google.auth.transport import requests

from src.utils.db_user import db_user
from src.utils.JWTGenerator import JWTGen

load_dotenv()

@signin_bp.route('/', methods=('GET', 'POST'))
def signin():
  if request.method == 'POST':
    if 'credential' in request.form:
      try:
        idinfo = id_token.verify_oauth2_token(request.form['credential'], requests.Request(), os.getenv("GOOGLE_OAUTH_KEY"))

        print(idinfo)

        google_sub = idinfo['sub']
        email = idinfo['email'].lower()

        if db_user.exists_google_sub(google_sub):
          session['user'] = db_user.get_user_from_google_sub(google_sub)

          return(redirect(url_for("home.index")))
        elif db_user.exists_email(email):
          db_user.link_google_sub(email, google_sub)
          
          session['user'] = db_user.get_user_from_google_sub(google_sub)

          return(redirect(url_for("home.index")))
        else:
          session['email'] = email
          session['google_sub'] = google_sub

          return(redirect(url_for("account.onboarding")))
      except ValueError:
        print("error!")
        return redirect(url_for("signin.signin"))
    
    if not request.form["email"]: return render_template('user/sign_in.html', invalid_email=True) 
    email = request.form["email"].lower()
    if db_user.exists_email(email):
      uuid = db_user.get_uuid_by_email(email)
      jwt = JWTGen.encode_jwt(email, uuid)
      print(jwt)
    else:
      jwt = JWTGen.encode_jwt(email)
      print(jwt)
    return render_template('user/sign_in.html', magic_link=True) 

  else: return render_template('user/sign_in.html')

@account_bp.route('/signout')
def signout():
  if 'user' in session: del session['user']
  return redirect(url_for('home.index'))

@account_bp.route('/verify/<jwt>')
def verify(jwt):
  if not jwt: return redirect(url_for('user/sign_in.html', invalid_link=True))
  claims = JWTGen.decode_jwt(jwt)
  if not claims: return redirect(url_for('user/sign_in.html', invalid_link=True))
  if 'uuid' in claims:
    session['user'] = db_user.get_user_from_uuid(claims['uuid'])

    return redirect(url_for("home.index"))
  elif 'email' in claims:
    session['email'] = claims['email']
    return redirect(url_for("account.onboarding"))
  
@account_bp.route('/onboarding', methods=('GET', 'POST'))
def onboarding():
  if request.method == 'POST':
    if 'email' not in session: return redirect(url_for('home.index'))
    if 'username' in request.form and len(request.form['username']) >= 1:
      email = session['email']
      del session['email']
      db_user.insert_user(request.form['username'][:20], email, session.get('google_sub', None))
      session['user'] = db_user.get_user_from_email(email)
      return redirect(url_for("home.index"))
    else: return render_template('user/onboarding.html', invalid_username = True)
  else:
    if 'email' in session: return render_template('user/onboarding.html')
    else: return redirect(url_for('home.index'))

