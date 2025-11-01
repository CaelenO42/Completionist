from src.dashboard import bp

from flask import render_template, request, session, redirect, url_for

@bp.route('/')
def index():
  if 'user' not in session: return redirect(url_for('home.index'))
  else: return render_template('dashboard.html')