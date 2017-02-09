import sqlite3
import os
import datetime

from google_credentials import GoogleCredentials
from gmail import Gmail
from contacts import Contacts

# q= rfc822msgid:kuku7@messages2gmail.com

if __name__ == '__main__':
	google_credentials = GoogleCredentials()
	google_credentials.authenticate()

#	gmail = Gmail(google_credentials.credentials)
#	date = datetime.datetime(2015, 2, 28, 7, 45)
#	msg = Gmail.create_message("<kuku7@messages2gmail.com>", "kuku", "kuku2", "kuku", date, "body")
#	gmail.insert_message(msg)

	contacts = Contacts(google_credentials.credentials)
	contacts.load_contacts()

	user_dir = os.path.expanduser('~')
	conn = sqlite3.connect(user_dir+'/backup_messages/chat.db')

	c = conn.cursor()

#	for row in c.execute('select text from message'):
#		print row

