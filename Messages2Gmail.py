import datetime, re

from google_credentials import GoogleCredentials
from gmail import Gmail
from contacts import Contacts
from MessagesDB import MessagesDB

# q= rfc822msgid:kuku7@messages2gmail.com

if __name__ == '__main__':
	google_credentials = GoogleCredentials()
	google_credentials.authenticate()

	gmail = Gmail(google_credentials.credentials)

	contacts = Contacts(google_credentials.credentials)
	contacts.load_contacts()

	MessagesDB = MessagesDB('/backup_messages_2017')

	# handle_id to Name cache
	handle_to_name = {}
	phone_number_reg = re.compile('^[a-z0-9\.\+ \(\)\+]+$')
	for handle in MessagesDB.get_handles():
		id = handle['id']
		if '@' in id:
			name = contacts.get_by_email(id)
		elif phone_number_reg.match(id):
			name = contacts.get_by_phone_number(id)
		if name:
			handle_to_name[handle['rowid']] = name
		else:
			handle_to_name[handle['rowid']] = id

	labels = gmail.get_labels("me")
	if 'Text' not in labels.keys():
		gmail.create_label("me", Gmail.make_label('Text'))

	i = 20
	for message in MessagesDB.get_messages(19285):
		date = datetime.datetime(2015, 2, 28, 7, 45)

		msg_id = '<%s_%s>' % (message['guid'], google_credentials.email)

		name = handle_to_name[message['handle_id']]
		if message['is_from_me']:
			sender = google_credentials.email
			to = name
		else:
			to = google_credentials.email
			sender = name

		subject = "Chat with %s"%name
		date = datetime.datetime.fromtimestamp(978307200 + message['date'])

		print msg_id
		print sender.encode('utf-8')
		print to.encode('utf-8')
		print name.encode('utf-8')
		print subject.encode('utf-8')
		if message['text']:
			print message['text'].encode('utf-8')

		msg = Gmail.create_message(msg_id, sender, to, subject, date, message['text'])
		gmail.insert_message(msg, labelIds=[labels['Text']])

		i -= 1
		if i==0:
			break
