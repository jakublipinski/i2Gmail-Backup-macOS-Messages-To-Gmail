import config

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GoogleCredentials:

    # Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
    OAUTH_SCOPES = ['https://www.googleapis.com/auth/userinfo.email',
                   'https://www.googleapis.com/auth/gmail.insert',
                   'https://www.googleapis.com/auth/gmail.labels',
                   'https://www.googleapis.com/auth/contacts.readonly',
                   'openid']

    def authenticate(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(config.TOKEN_FILE):
            with open(config.TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(config.CLIENT_SECRET_FILE, GoogleCredentials.OAUTH_SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(config.TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)

        self.credentials = creds
