import time

import base64, io
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import googleapiclient
import mimetypes

import httplib2
from apiclient import discovery, errors

class Gmail:

    def __init__(self, credentials):
        # Authorize the httplib2.Http object with our credentials
        http = credentials.authorize(httplib2.Http())

        # Build the Gmail service from discovery
        self.gmail_client = discovery.build('gmail', 'v1', http=http)

    def insert_message(self, message, user_id='me', threadId=None, labelIds=None):
        try:
            print 'Message size: %d' % len(message['raw'])

            if len(message['raw']) < 2000000:
                if threadId:
                    message['threadId'] = threadId
                if labelIds:
                    message['labelIds'] = labelIds

                message = self.gmail_client.users().messages().insert(
                    userId=user_id, body=message, internalDateSource="dateHeader").execute()
            else:
                b = io.BytesIO()
                message_bytes = base64.urlsafe_b64decode(str(message['raw']))
                b.write(message_bytes)
                body = {}
                if threadId:
                    body['threadId'] = threadId
                if labelIds:
                    body['labelIds'] = labelIds
                media_body = googleapiclient.http.MediaIoBaseUpload(b,
                                                    mimetype='message/rfc822')
                message = self.gmail_client.users().messages().insert(userId=user_id,
                                                    body=body,
                                                    internalDateSource="dateHeader",
                                                    media_body=media_body).execute()

            print('Message Id: %s' % message['id'])
            return message
        except errors.HttpError, error:
            print('An error occurred: %s' % error)
            raise

    @staticmethod
    def create_message_with_attachments(id, sender, to, subject, date, message_text,
                                       attachments, in_reply_to=None, references=None,
                                        extra_headers = None):
        if attachments:
            message = MIMEMultipart()
        else:
            message = MIMEText(
                message_text.encode('utf-8') if message_text else '', 'plain',
                'utf-8')

        message['Message-id'] = id
        if in_reply_to:
            message['In-Reply-To'] = in_reply_to
        if references:
            message['References'] = references
        message['From'] = sender.encode('utf-8')
        message['To'] = to.encode('utf-8')
        message['Subject'] = subject.encode('utf-8')

        message['Date'] = formatdate(time.mktime(date.timetuple()))

        if extra_headers:
            for key, value in extra_headers.iteritems():
                message[key] = value

        if attachments:
            msg = MIMEText(message_text.encode('utf-8') if message_text else '', 'plain', 'utf-8')
            message.attach(msg)

            for attachment in attachments:

                filename = attachment['filename']
                content_type = attachment['mime_type']
                transfer_name = attachment['transfer_name']

                if content_type is None:
                    content_type, encoding = mimetypes.guess_type(filename)

                if content_type is None:
                    content_type = 'application/octet-stream'

                main_type, sub_type = content_type.split('/', 1)
                if main_type == 'text':
                    fp = open(filename, 'rb')
                    msg = MIMEText(fp.read(), _subtype=sub_type)
                    fp.close()
                elif main_type == 'image':
                    fp = open(filename, 'rb')
                    msg = MIMEImage(fp.read(), _subtype=sub_type)
                    fp.close()
                elif main_type == 'audio':
                    fp = open(filename, 'rb')
                    msg = MIMEAudio(fp.read(), _subtype=sub_type)
                    fp.close()
                else:
                    fp = open(filename, 'rb')
                    msg = MIMEBase(main_type, sub_type)
                    msg.set_payload(fp.read())
                    fp.close()

                msg.add_header('Content-Disposition', 'attachment', filename=transfer_name)
                message.attach(msg)

        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def create_label(self, user_id, label_object):
        """Creates a new label within user's mailbox, also prints Label ID.

        Args:
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            label_object: label to be added.

        Returns:
            Created Label.
        """
        try:
            label = self.gmail_client.users().labels().create(userId=user_id,
                                                body=label_object).execute()
            print label['id']
            return label
        except errors.HttpError, error:
            print 'An error occurred: %s' % error

    @staticmethod
    def make_label(label_name, mlv='show', llv='labelShow'):
        """Create Label object.

        Args:
            label_name: The name of the Label.
            mlv: Message list visibility, show/hide.
            llv: Label list visibility, labelShow/labelHide.

        Returns:
            Created Label.
        """
        label = {'messageListVisibility': mlv,
               'name': label_name,
               'labelListVisibility': llv}
        return label

    def get_labels(self, user_id):
        """Get a list all labels in the user's mailbox.

        Args:
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
        Returns:
            A list all Labels in the user's mailbox.
        """
        try:
            response = self.gmail_client.users().labels().list(userId=user_id).execute()
            labels = response['labels']
            ret = {}
            for label in labels:
                ret[label['name']] = label['id']
            return ret
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
