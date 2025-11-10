from src.utils.db_conn import db_conn

class db_task:
  def get_tasks(uuid):
    """Returns a list of tasks for the user UUID"""
    with db_conn() as curr:
      curr.execute("SELECT * FROM task WHERE uuid = %s;", (uuid,))
      res = curr.fetchall()
      return res

  def get_task(taskID):
    pass