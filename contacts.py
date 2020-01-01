import gdata.data
import gdata.contacts.client
import gdata.contacts.data

import string

import config

class Contacts:

	def __init__(self, credentials):
		auth2token = gdata.gauth.OAuth2Token(client_id=credentials.client_id,
											 client_secret=credentials.client_secret,
											 scope='https://www.google.com/m8/feeds/contacts/default/full',
											 access_token=credentials.access_token,
											 refresh_token=credentials.refresh_token,
											 user_agent=config.APPLICATION_NAME)
		self.client = gdata.contacts.client.ContactsClient()
		auth2token.authorize(self.client)

		self.email_to_name = {}
		self.phone_to_name = {}

	def load_contacts(self):
		max_results = 99999
		start_index = 1
		query = gdata.contacts.client.ContactsQuery()
		query.max_results = max_results
		query.start_index = start_index

		feed = self.client.GetContacts(q=query)
		for i, entry in enumerate(feed.entry):
			if entry.name:
				full_name = entry.name.full_name.text

				primary_email = None
				for email_entry in entry.email:
					email = email_entry.address.lower()
					if email_entry.primary and email_entry.primary=="true":
						primary_email = email
					if email in self.email_to_name:
						print(u"Email address: '{}' is assigned to both '{}' and '{}'!".\
							format(email, self.email_to_name[email], full_name))
					else:
						self.email_to_name[email] = (full_name, u'%s <%s>' % (full_name, email))

				for phone_number_entry in entry.phone_number:
					phone_number = Contacts.strip_and_reverse_phone_number(phone_number_entry.text)
					if phone_number in self.phone_to_name:
						print("Phone number: '%s' is assigned to both '%s' and '%s'!"%
							  (phone_number_entry.text, self.phone_to_name[phone_number], full_name))
					else:
						if primary_email:
							self.phone_to_name[phone_number] = (
							full_name, u'%s <%s>' % (full_name, primary_email))
						else:
							self.phone_to_name[phone_number] = (full_name, u'%s <%s>' % (full_name, phone_number_entry.text))

	def get_by_phone_number(self, phone_number):
		phone_number = Contacts.strip_and_reverse_phone_number(phone_number)
		return self.phone_to_name.get(phone_number)

	def get_by_email(self, email):
		email = email.lower()
		return self.email_to_name.get(email)

	@staticmethod
	def strip_and_reverse_phone_number(phone_number):
		number = ''.join(ch for ch in phone_number if ch.isdigit())
		if len(number)<3:
			return phone_number
		number = number[-9:]
		number = number[::-1]
		return number

