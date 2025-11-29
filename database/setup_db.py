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
      email TEXT UNIQUE NOT NULL,
      google_sub NUMERIC(21) UNIQUE
    );
    """)
  
  curr.execute(
    """
    CREATE TABLE IF NOT EXISTS category (
      uuid UUID DEFAULT gen_random_uuid() PRIMARY KEY,
      name TEXT NOT NULL,
      color TEXT NOT NULL,
      user_id UUID NOT NULL REFERENCES user_account(uuid)
    );
    """
  )

  curr.execute(
    """
    CREATE TABLE IF NOT EXISTS task (
      uuid UUID DEFAULT gen_random_uuid() PRIMARY KEY,
      title TEXT NOT NULL,
      due_date DATE,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
      status TEXT NOT NULL DEFAULT 'planned',
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
    CREATE OR REPLACE FUNCTION maintain_task_sequence()
    RETURNS TRIGGER AS $$
    DECLARE
      max_pos INT;
      old_pos INT;
      new_pos INT;
    BEGIN
      IF current_setting('task.skip_reorder', true) = 'true' THEN
        IF TG_OP = 'DELETE' THEN
          RETURN OLD;
        ELSE
          RETURN NEW;
        END IF;
      END IF;

      IF TG_OP IN ('INSERT', 'UPDATE') THEN
        SELECT COALESCE(MAX(position), 0) INTO max_pos
        FROM task
        WHERE user_id = NEW.user_id;
      END IF;

      IF TG_OP = 'INSERT' THEN
        NEW.position = max_pos + 1;
          
      ELSIF TG_OP = 'UPDATE' AND NEW.position IS NOT NULL THEN
        old_pos := OLD.position;
        new_pos := NEW.position;

        IF old_pos IS DISTINCT FROM new_pos THEN
          
          IF new_pos < 1 OR new_pos > max_pos THEN
            new_pos := max_pos; 
          END IF;
          
          IF old_pos > new_pos OR old_pos < new_pos THEN
            PERFORM set_config('task.skip_reorder', 'true', false);

            IF old_pos > new_pos THEN
              UPDATE task
              SET position = position + 1
              WHERE user_id = NEW.user_id
                AND position >= new_pos
                AND position < old_pos
                AND id <> NEW.id;
            ELSIF old_pos < new_pos THEN
              UPDATE task
              SET position = position - 1
              WHERE user_id = NEW.user_id
                AND position > old_pos
                AND position <= new_pos
                AND id <> NEW.id;
            END IF;

            PERFORM set_config('task.skip_reorder', 'false', false);
          END IF;

          NEW.position = new_pos; 
        END IF;

      ELSIF TG_OP = 'DELETE' THEN
        PERFORM set_config('task.skip_reorder', 'true', false);

        UPDATE task
        SET position = position - 1
        WHERE user_id = OLD.user_id
          AND position > OLD.position;
          
        PERFORM set_config('task.skip_reorder', 'false', false);
      END IF;

      IF TG_OP = 'DELETE' THEN
        RETURN OLD;
      ELSE
        RETURN NEW;
      END IF;

    END;
    $$ LANGUAGE plpgsql;
    """)

  curr.execute(
    """
    DROP TRIGGER IF EXISTS maintain_task_sequence_trigger 
      ON task;
    """)

  curr.execute(
    """
    CREATE TRIGGER maintain_task_sequence_trigger 
      BEFORE INSERT OR UPDATE OR DELETE ON task 
      FOR EACH ROW EXECUTE FUNCTION maintain_task_sequence();
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