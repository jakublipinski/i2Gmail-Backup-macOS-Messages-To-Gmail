import os
import config
import sqlite3


class MessagesDB:

	def __init__(self, path = config.DEFAULT_MESSAGES_PATH):
		user_dir = os.path.expanduser('~')
		self.path = path.replace('~', user_dir)
		print self.path + 'chat.db'
		self.conn = sqlite3.connect(self.path + 'chat.db')

	def get_handles(self):
		for row in self.conn.cursor().execute('select ROWID, id from handle'):
			yield {'rowid':row[0], 'id':row[1]}

	def get_messages(self, last_processed_rowid = 0):

		attachments = []
		c = self.conn.cursor().execute(
				'select message.ROWID, message.guid, message.text, message.handle_id, message.service, message.date, message.is_from_me, '
				'attachment.filename, attachment.mime_type, attachment.transfer_name ' \
				'from message '
				'left OUTER JOIN message_attachment_join on message.ROWID = message_attachment_join.message_id '
				'left OUTER join attachment on message_attachment_join.attachment_id = attachment.ROWID '\
				'where message.ROWID>? and handle_id>0 '\
				'order by message.ROWID',(last_processed_rowid,))
		msg = {'rowid':-1}
		row = c.fetchone()
		while row:
			if msg['rowid'] != row[0]:
				msg = {'rowid': row[0], 'guid': row[1], 'text': row[2],
				 'handle_id': row[3],
				 'service': row[4], 'date': row[5], 'is_from_me': row[6],
				 'attachments' : [] }
			if row[7]:
				filename = row[7]
				if self.path != config.DEFAULT_MESSAGES_PATH:
					filename = self.path + filename[-len(filename)+len(config.DEFAULT_MESSAGES_PATH):]
				msg['attachments'].append({'filename': filename, 'mime_type':row[8],
										   'transfer_name':row[9]})
			row = c.fetchone()
			if not row or msg['rowid'] != row[0]:
				yield msg
