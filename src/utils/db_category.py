from src.utils.db_conn import db_conn

class db_category:
  def get_categories(user_uuid):
    with db_conn() as curr:
      curr.execute("SELECT * FROM category WHERE user_id = %s", (user_uuid,))
      res = [dict(row) for row in curr.fetchall()]
      return res
  
  def get_category(user_uuid, category_uuid):
    with db_conn() as curr:
      curr.execute("SELECT 1 FROM category WHERE user_id = %s AND uuid = %s;", (user_uuid, category_uuid,))
      res = dict(curr.fetchone())
      return res
    
  def new_category(user_uuid, data):
    with db_conn() as curr:
      curr.execute("""
        INSERT INTO category (
          name,
          color,
          user_id)
        VALUES (%s, %s, %s)
        RETURNING *;
        """, (data.get('name'), data.get('color').replace("#", ""), user_uuid,))
      res = dict(curr.fetchone())
      return res
    
  def delete_category(user_uuid, category_uuid):
    with db_conn() as curr:
      curr.execute("""
        DELETE FROM category 
        WHERE
          uuid = %s AND user_id = %s;
        """, (category_uuid, user_uuid,));
  
  def delete_categories(user_uuid):
    with db_conn() as curr:
      curr.execute("""
        DELETE FROM category 
        WHERE
          user_id = %s;
        """, (user_uuid,));
  
  def set_category(user_uuid, category_uuid, data):
    with db_conn() as curr:
      curr.execute("""
        UPDATE category 
        SET
          name = COALESCE(NULLIF(%s, ''), name), 
          color = COALESCE(NULLIF(%s, ''), color)
        WHERE
          uuid = %s AND user_id = %s;
        """, (data.get('name'), data.get('color'), category_uuid, user_uuid,))
      

  def is_category_owner(user_uuid, category_uuid):
    with db_conn() as curr:
      curr.execute("SELECT 1 FROM category WHERE uuid = %s AND user_id = %s;", (category_uuid, user_uuid))
      res = curr.fetchall()
      if res: return True
      return False