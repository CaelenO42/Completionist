import database.setup_db as db
from src.utils.JWTGenerator import JWTGen
from src.utils.MailSender import MailSender

import os

print("Setting up database...")
db.setup_db()

print("Generating JWT Key...")
JWTGen.generate_key()

if os.path.exists(".env"): print(".env already exists! Skipping...")
else:
  env_data = "FLASK_APP=src\nFLASK_ENV=development\n"

  val = input("Enter google OAuth key (enter to skip): ")
  if len(val) > 0: env_data += f"\nGOOGLE_OAUTH_KEY = {val}"
  else: print("No Google OAuth key provided! Sign in with Google will be disabled until you provide a GOOGLE_OAUTH_KEY in the .env file.")

  val = input("Enter Gmail Credentials Path (enter to skip): ")
  if len(val) > 0: 
    env_data += f"\nGOOGLE_APPLICATION_CREDENTIALS = {val}"
    print("Follow the link to generate your gmail token.")
    MailSender.get_service(val)
  else: print("No Gmail Credentials Provided! Sending mail with Gmail will be disabled and JWT links will print in console instead.")

  with open('.env', 'w') as f:
    f.write(env_data)

  print("Created .env file!")