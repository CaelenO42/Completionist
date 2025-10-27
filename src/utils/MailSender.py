import base64
import os
from dotenv import load_dotenv

from email.message import EmailMessage

import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

class MailSender():
  def get_service(client_file = os.getenv("GOOGLE_OAUTH_KEY")):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("google_email_token.json"):
      creds = Credentials.from_authorized_user_file("google_email_token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            client_file, SCOPES
        )
        creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open("google_email_token.json", "w") as token:
        token.write(creds.to_json())
      
    service = build('gmail', 'v1', credentials=creds)
    return service
  
  def send_mail(recipient, subject, content, rich_content):
    service = MailSender.get_service()
    
    message = EmailMessage()

    message.set_content(content)
    message.add_alternative(rich_content, subtype='html')

    message["To"] = recipient
    message["From"] = "completionist.csuf@gmail.com"
    message["Subject"] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'raw': encoded_message}

    try:
      send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
      ).execute()
      # print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
      print(f"An error occurred: {error}")
      send_message = None
    return send_message
  
  def verification_email(email, jwt):
    plain_content = f"To log into Completionist, please go to the link below:\n\nhttp://localhost:5000/account/verify/{jwt}\n\nIf you did not request to sign in, you can safely ignore this message.\n\nThank you for using Completionist!"
    rich_content = f"""
    <h3>To log into Completionist, please follow the link below:</h3>
    <a href="http://localhost:5000/account/verify/{jwt}">Log In</a>
    <p>If the button above is not working, copy and paste the following link into your browser:</p>
    <p>http://localhost:5000/account/verify/{jwt}</p>
    <p><strong>If you did not request to sign in, you can safely ignore this message.</strong></p>
    <p><i>Thank you for using Completionist!</i></p>
    """

    MailSender.send_mail(email, "Log In to Completionist", plain_content, rich_content)