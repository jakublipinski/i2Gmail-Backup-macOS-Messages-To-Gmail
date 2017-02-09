import datetime

from google_credentials import GoogleCredentials
from gmail import Gmail
from contacts import Contacts
from MessagesDB import MessagesDB

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

	MessagesDB = MessagesDB('/backup_messages')

	# ROWID to Name cache
	rowid_to_name = {}
	for handle in MessagesDB.get_handles():
		if '@' in handle['id']:
			name = contacts.get_by_email(handle['id'])
		else:
			name = contacts.get_by_phone_number(handle['id'])
		if name:
			rowid_to_name[handle['rowid']] = name

