import time

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import mimetypes

import httplib2
from apiclient import discovery


class Gmail:

    def __init__(self, credentials):
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
