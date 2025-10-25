import psycopg2

def exists_database(db_name):
  """Return True if database already exists, False otherwise"""
  conn = psycopg2.connect(database='postgres')
  curr = conn.cursor()
  curr.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;",
              (db_name,))
  res = curr.fetchall()
  conn.close()

  if res:
    return True
  return False

def create_database(db_name):
  """Create a database in postgres"""
  conn = psycopg2.connect(database='postgres')
  curr = conn.cursor()
  conn.autocommit = True
  curr.execute(f"CREATE DATABASE {db_name};")
  conn.close()

def create_schema(db_name):
  """Create tables, functions, and triggers in the database"""
  conn = psycopg2.connect(database=db_name)
  curr = conn.cursor()

  # ---------------------------------------------------------------------------- #
  #                                    TABLES                                    #
  # ---------------------------------------------------------------------------- #

  curr.execute(
    """
    CREATE TABLE IF NOT EXISTS user_account (
      uuid UUID DEFAULT gen_random_uuid() PRIMARY KEY,
      username VARCHAR(20) NOT NULL,
      email TEXT NOT NULL,
      google_sub NUMERIC(21)
    );
    """)
  
  curr.execute(
    """
    CREATE TABLE IF NOT EXISTS category (
      uuid UUID DEFAULT gen_random_uuid() PRIMARY KEY,
      name TEXT NOT NULL,
      user_id UUID NOT NULL REFERENCES user_account(uuid)
    );
    """
  )

  curr.execute(
    """
    CREATE TABLE IF NOT EXISTS task (
      uuid UUID DEFAULT gen_random_uuid() PRIMARY KEY,
      title TEXT,
      due_date DATE,
      created_at DATE DEFAULT now(),
      status TEXT NOT NULL,
      position INT NOT NULL,
      user_id UUID NOT NULL REFERENCES user_account(uuid),
      category_id UUID REFERENCES category(uuid)
    );
    """)

  # ---------------------------------------------------------------------------- #
  #                                   TRIGGERS                                   #
  # ---------------------------------------------------------------------------- #

  # --------------------------- Update Task Rank --------------------------- #
  curr.execute(
    """
    CREATE OR REPLACE FUNCTION set_new_task_position()
    RETURNS TRIGGER AS $$
    BEGIN
      SELECT COALESCE(COUNT(*), 0) + 1
      FROM task
      WHERE user_id = NEW.user_id
      INTO NEW.position;
      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

  curr.execute(
    """
    DROP TRIGGER IF EXISTS task_position_trigger 
      ON task;
    """)

  curr.execute(
    """
    CREATE TRIGGER task_position_trigger 
      BEFORE INSERT ON task 
      FOR EACH ROW 
      EXECUTE FUNCTION set_new_task_position();
    """)

  # Commit and close connection
  conn.commit()
  conn.close()

def setup_db():
  DB_NAME = "completionist"
  if not exists_database(DB_NAME):
    create_database(DB_NAME)
  create_schema(DB_NAME)

if __name__ == "__main__":
  setup_db()