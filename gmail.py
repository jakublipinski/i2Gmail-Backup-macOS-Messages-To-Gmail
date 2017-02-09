from __future__ import print_function
import httplib2
import os
import config

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from apiclient import errors

import datetime, time

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import mimetypes

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class Gmail:

    # Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
    OAUTH_SCOPE = ['https://www.googleapis.com/auth/gmail.insert',]

    def __init__(self):
        self.gmail_client = None

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """

        store = oauth2client.file.Storage(config.CREDENTIALS_STORAGE_FILE)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(config.CLIENT_SECRET_FILE,
                                                  self.OAUTH_SCOPE)
            flow.user_agent = config.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + config.CREDENTIALS_STORAGE_FILE)
        return credentials

    def connect(self):
        credentials = self.get_credentials()

        # Authorize the httplib2.Http object with our credentials
        http = credentials.authorize(httplib2.Http())

        # Build the Gmail service from discovery
        self.gmail_client = discovery.build('gmail', 'v1', http=http)

    def insert_message(self, message, user_id='me'):
        try:
            message = self.gmail_client.users().messages().insert(
                userId=user_id, body=message, internalDateSource="dateHeader").execute()
            print('Message Id: %s' % message['id'])
            return message
        except errors.HttpError, error:
            print('An error occurred: %s' % error)

    @staticmethod
    def create_message(id, sender, to, subject, date, message_text):
        message = MIMEText(message_text)
        message['Message-id'] = id
        message['From'] = sender
        message['To'] = to
        message['Subject'] = subject
        message['Date'] = formatdate(time.mktime(date.timetuple()))
        return {'raw': base64.b64encode(message.as_string())}

    @staticmethod
    def create_message_with_attachment(self, sender, to, subject, message_text,
                                       file_dir, filename):
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        msg = MIMEText(message_text)
        message.attach(msg)

        path = os.path.join(file_dir, filename)
        content_type, encoding = mimetypes.guess_type(path)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(path, 'rb')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(path, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(path, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(path, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()

        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

        return {'raw': base64.b64encode(message.as_string())}
