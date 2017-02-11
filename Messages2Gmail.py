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

	MessagesDB = MessagesDB('~/backup_messages_2017/')

	# handle_id to Name cache
	handle_to_name = {}
	phone_number_reg = re.compile('^[a-z0-9\.\+ \(\)\+]+$')
	for handle in MessagesDB.get_handles():
		id = handle['id']
		if '@' in id:
			names = contacts.get_by_email(id)
		elif phone_number_reg.match(id):
			names = contacts.get_by_phone_number(id)
		if names:
			handle_to_name[handle['rowid']] = names
		else:
			handle_to_name[handle['rowid']] = (id, id)

	labels = gmail.get_labels("me")
	if 'Text' not in labels.keys():
		gmail.create_label("me", Gmail.make_label('Text'))

	threads = {}
	for message in MessagesDB.get_messages(19285):

		print message

		msg_id = '<%s_%s>' % (message['guid'], google_credentials.email)
		date = datetime.datetime.fromtimestamp(978307200 + message['date'])

		names = ''
		names_and_addressess = ''
		thread_key = '%s' % date.strftime("%d%m%Y")

		chat_handles = list(message['chat_handles'])
		chat_handles.sort()
		no_of_handles = len(chat_handles)
		for i in range(0, no_of_handles):
			handle_id = chat_handles[i]
			thread_key += '_%s' % handle_id
			name, name_and_address = handle_to_name[handle_id]
			print '%s %s %s' % (handle_id, name, name_and_address)
			if i == no_of_handles-1: # last element
				names += name
				names_and_addressess += name_and_address
			elif i == no_of_handles-2: # one before last handle
				names += name + ' and '
				names_and_addressess += name_and_address+'; '
			else:
				names += name + ', '
				names_and_addressess += name_and_address+'; '

		print thread_key

		if message['is_from_me']:
			sender = google_credentials.email
			to = names_and_addressess
		else:
			to = google_credentials.email
			name, name_and_address = handle_to_name[message['handle_id']]
			sender = name_and_address

		subject = "Chat with %s" % (names)

		thread = threads.get(thread_key, {"thread_id":None, "in_reply_to":None})

		print sender.encode('utf-8')
		print to.encode('utf-8')
		print subject.encode('utf-8')
		if message['text']:
			print message['text'].encode('utf-8')
		if message['attachments']:
			print message['attachments']
		print

		msg = Gmail.create_message_with_attachments(msg_id, sender, to, subject, date, message['text'], message['attachments'],
								   in_reply_to=thread['in_reply_to'], references=thread['in_reply_to'])

		msg = gmail.insert_message(msg, labelIds=[labels['Text']], threadId=thread['thread_id'])

		threads[thread_key] = {"thread_id":msg['threadId'], "in_reply_to":msg['id']}
