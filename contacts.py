import atom.data
import gdata.data
import gdata.contacts.client
import gdata.contacts.data

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

	def PrintAllContacts(self):
	  feed = self.client.GetContacts()
	  for i, entry in enumerate(feed.entry):
		if entry.name:
		  print '\n%s %s' % (i+1, entry.name.full_name.text)
		if entry.content:
		  print '    %s' % (entry.content.text)
		# Display the primary email address for the contact.
		for email in entry.email:
		  if email.primary and email.primary == 'true':
			print '    %s' % (email.address)
		# Show the contact groups that this contact is a member of.
		for group in entry.group_membership_info:
		  print '    Member of group: %s' % (group.href)
		# Display extended properties.
		for extended_property in entry.extended_property:
		  if extended_property.value:
			value = extended_property.value
		  else:
			value = extended_property.GetXmlBlob()
		  print '    Extended Property - %s: %s' % (extended_property.name, value)