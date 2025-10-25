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
  def get_service():
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
            "google_email_creds.json", SCOPES
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
      print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
      print(f"An error occurred: {error}")
      send_message = None
    return send_message