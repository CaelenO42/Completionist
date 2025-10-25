from src.utils.db_conn import db_conn

import random

class db_user:
  def exists_google_sub(google_sub):
    """Returns True if the google_sub exists in the database, False otherwise"""
    with db_conn() as curr:
      curr.execute("SELECT 1 FROM user_account WHERE google_sub = %s;", (google_sub,))
      res = curr.fetchall()
      if res: return True
      return False
    
  def exists_email(email):
    """Returns True if the email exists in the database, False otherwise"""
    with db_conn() as curr:
      curr.execute("SELECT 1 FROM user_account WHERE email = %s;", (email,))
      res = curr.fetchall()
      if res: return True
      return False
    
  def link_google_sub(email, google_sub):
    with db_conn() as curr:
      if not db_conn.exists_google_sub(google_sub):
        curr.execute("UPDATE user_account SET google_sub = %s WHERE email = %s;", (google_sub, email))
    
  def insert_user(username, email, google_sub=None):
    """Inserts a new user into the database"""
    if google_sub:
      with db_conn() as curr:
        curr.execute(
          """
          INSERT INTO user_account (
            username,
            email,
            google_sub)
          VALUES (%s, %s, %s);
          """,
          (username[:20], email.lower(), google_sub))
    else:
      with db_conn() as curr:
        curr.execute(
          """
          INSERT INTO user_account (
            username,
            email)
          VALUES (%s, %s);
          """,
          (username[:20], email.lower()))
        
  def get_uuid_by_email(email):
    with db_conn() as curr:
      curr.execute("SELECT uuid FROM user_account WHERE email = %s;", (email.lower(),))
      res = curr.fetchone()
      return res[0]
    
  def get_user_from_uuid(uuid):
    with db_conn() as curr:
      curr.execute(
        """
        SELECT  uuid,
                username,
                email,
                google_sub
        FROM user_account
        WHERE uuid = %s;
        """, (uuid,))
      
      res = curr.fetchone()
      user = {
        'uuid': res[0],
        'username': res[1],
        'email': res[2],
        'google_sub': res[3]
      }

      return user
      
  def get_user_from_google_sub(google_sub):
    with db_conn() as curr:
      curr.execute(
        """
        SELECT  uuid,
                username,
                email,
                google_sub
        FROM user_account
        WHERE google_sub = %s;
        """, (google_sub,))
      
      res = curr.fetchone()
      user = {
        'uuid': res[0],
        'username': res[1],
        'email': res[2],
        'google_sub': res[3]
      }

      return user