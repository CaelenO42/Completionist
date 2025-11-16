import csv
import os

import psycopg2

from db_conn import db_conn
from setup_db import setup_db

def drop_database(db_name):
  """Drop the gamescout database"""
  conn = psycopg2.connect(database='postgres')
  curr = conn.cursor()
  conn.autocommit = True
  curr.execute(f"DROP DATABASE {db_name};")
  conn.commit()
  conn.close()

if __name__ == "__main__":
  DB_NAME = "completionist"
  drop_database(DB_NAME)
  setup_db()