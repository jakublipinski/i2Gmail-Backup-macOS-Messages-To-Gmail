# -*- coding:utf-8 -*-
import datetime, re

from google_credentials import GoogleCredentials
from gmail import Gmail
from contacts import Contacts
from MessagesDB import MessagesDB
import json
import config

settings = {}


def save_settings():
	with open(config.SETTINGS_FILE, 'w') as f:
		json.dump(settings, f, indent=4)


def load_settings():
	try:
		with open(config.SETTINGS_FILE, 'r') as f:
			return json.load(f)
	except Exception as e:
		print(e)
		print('can''t load settings, do you want to reset it?')
		# comment out the line bellow to reset the settings
		raise e
		return {'last_rowid' : 0, 'threads': {} }

if __name__ == '__main__':
	google_credentials = GoogleCredentials()
	google_credentials.authenticate()

	gmail = Gmail(google_credentials.credentials)

	contacts = Contacts(google_credentials.credentials)
	contacts.load_contacts()

	MessagesDB = MessagesDB()

	# handle_id to Name cache
	handle_to_name = {}
	handle_to_id = {}
	phone_number_reg = re.compile('^[a-z0-9\.\+ \(\)\+]+$')
	for handle in MessagesDB.get_handles():
		id = handle['id']
		handle_to_id[handle['rowid']] = id
		if '@' in id:
			names = contacts.get_by_email(id)
		elif phone_number_reg.match(id):
			names = contacts.get_by_phone_number(id)
		if names:
			handle_to_name[handle['rowid']] = names
		else:
			handle_to_name[handle['rowid']] = (id, id)

	if contacts.get_by_email(google_credentials.email):
		me = contacts.get_by_email(google_credentials.email)[1]
	else:
		me = google_credentials.email

	labels = gmail.get_labels("me")
	if config.GMAIL_LABEL not in labels.keys():
		gmail.create_label("me", Gmail.make_label(config.GMAIL_LABEL))

	settings = load_settings()

	for message in MessagesDB.get_messages(settings['last_rowid']):

		print(message)

		msg_id = '<%s_%s>' % (message['guid'], google_credentials.email)
		date = datetime.datetime.fromtimestamp(978307200 + message['date']/1000000000)

		names = ''
		names_and_addressess = ''
		thread_key = '%s' % date.strftime("%d%m%Y")

		original_bearer = ''
		chat_handles = list(message['chat_handles'])
		chat_handles.sort()
		no_of_handles = len(chat_handles)
		for i in range(0, no_of_handles):
			handle_id = chat_handles[i]
			thread_key += '_%s' % handle_id
			name, name_and_address = handle_to_name[handle_id]
			print('%s %s %s'.format (handle_id, name.encode('utf-8'), name_and_address.encode('utf-8')))
			if i == no_of_handles-1: # last element
				names += name
				names_and_addressess += name_and_address
				original_bearer += handle_to_id[handle_id]
			elif i == no_of_handles-2: # one before last handle
				names += name + ' and '
				names_and_addressess += name_and_address+'; '
				original_bearer += handle_to_id[handle_id]+', '
			else:
				names += name + ', '
				names_and_addressess += name_and_address+'; '
				original_bearer += handle_to_id[handle_id]+', '

		print(thread_key)

		if message['is_from_me']:
			sender = me
			to = names_and_addressess
			original_bearer = 'Sent via %s from %s to %s' % (message['service'],
								'me', original_bearer)

		else:
			to = me
			name, name_and_address = handle_to_name[message['handle_id']]
			sender = name_and_address
			original_bearer = 'Sent via %s from %s to %s' % (message['service'],
								handle_to_id[message['handle_id']], original_bearer)

		subject = "Chat with %s" % (names)

		thread = settings['threads'].get(thread_key, {"thread_id":None, "in_reply_to":None})

		print(sender.encode('utf-8'))
		print(to.encode('utf-8'))
		print(date)
		print(subject.encode('utf-8'))
		if message['text']:
			print(message['text'].encode('utf-8'))
		if message['attachments']:
			print(message['attachments'])

		msgs = Gmail.create_messages_with_attachments(msg_id, sender, to, subject, date, message['text'], message['attachments'],
								   in_reply_to=thread['in_reply_to'], references=thread['in_reply_to'],
								   extra_headers = {'X-Original-Bearer' : original_bearer,
													'X-Mailer': 'Backup macOS Messages to Gmail; visit: https://github.com/jakublipinski/i2Gmail-Backup-macOS-Messages-To-Gmail'})

		for msg in msgs:
			msg = gmail.insert_message(msg, labelIds=[labels[config.GMAIL_LABEL]], threadId=thread['thread_id'])

			settings['threads'][thread_key] = {"thread_id":msg['threadId'], "in_reply_to":msg['id']}
			print

		settings['last_rowid'] = message['rowid']
		save_settings()