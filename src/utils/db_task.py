from src.utils.db_conn import db_conn

class db_task:
  @staticmethod
  def get_tasks(user_uuid):
    """Returns a list of tasks for the user UUID"""
    with db_conn() as curr:
      curr.execute("SELECT * FROM task WHERE user_id = %s;", (user_uuid,))
      res = [dict(row) for row in curr.fetchall()]
      return res

  def get_task(user_uuid, task_uuid):
    with db_conn() as curr:
      curr.execute("SELECT * FROM task WHERE user_id = %s AND uuid = %s;", (user_uuid, task_uuid,))
      res = dict(curr.fetchone())
      return res

  def new_task(user_uuid, task):
    with db_conn() as curr:
      curr.execute("""
        INSERT INTO task (
          title, 
          status, 
          due_date,
          category_id,
          user_id) 
        VALUES (%s, %s, %s, %s, %s)
        RETURNING uuid;
        """, (task.get('title'), task.get('status'), task.get('due_date'), task.get('category_id'), user_uuid,))
      res = curr.fetchone()
      return res[0]

  def set_task(user_uuid, task_uuid, task):
    with db_conn() as curr:
      curr.execute("""
        UPDATE task 
        SET
          title = %s, 
          due_date = %s,
          status = %s, 
          position = COALESCE(NULLIF(%s, '')::int, position),
          category_id = %s
        WHERE
          uuid = %s AND user_id = %s;
        """, (task.get('title'), task.get('due_date'), task.get('status'), task.get('position'), task.get('category_id'), task_uuid, user_uuid,))
      
  def delete_task(user_uuid, task_uuid):
    with db_conn() as curr:
      curr.execute("""
        DELETE FROM task 
        WHERE
          uuid = %s AND user_id = %s;
        """, (task_uuid, user_uuid,));
  
  def delete_tasks(user_uuid):
    with db_conn() as curr:
      curr.execute("""
        DELETE FROM task 
        WHERE
          user_id = %s;
        """, (user_uuid,));

  def is_task_owner(user_uuid, task_uuid):
    with db_conn() as curr:
      curr.execute("SELECT 1 FROM task WHERE uuid = %s AND user_id = %s;", (task_uuid, user_uuid))
      res = curr.fetchall()
      if res: return True
      return False