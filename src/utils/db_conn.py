"""Context manager used to connect to the PostgreSQL database"""
import psycopg2
from psycopg2.extras import DictCursor

class db_conn:
  def __enter__(self):
    self.conn = psycopg2.connect(database='completionist')
    self.curr = self.conn.cursor(cursor_factory=DictCursor)
    return self.curr

  def __exit__(self, exc_type, exc_value, exc_tb):
    self.conn.commit()
    self.conn.close()