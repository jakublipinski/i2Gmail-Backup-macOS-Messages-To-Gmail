import os
import config
import sqlite3


class MessagesDB:

	def __init__(self, path = config.DEFAULT_MESSAGES_PATH):
		self.user_dir = os.path.expanduser('~')
		self.path = path.replace('~', self.user_dir)
		self.config_path = config.DEFAULT_MESSAGES_PATH.replace('~', self.user_dir)
		self.conn = sqlite3.connect(self.path + 'chat.db')
		self.conn.row_factory = sqlite3.Row

	def get_handles(self):
		for row in self.conn.cursor().execute('select ROWID, id from handle'):
			yield {'rowid':row[0], 'id':row[1]}

	def get_messages(self, last_processed_rowid = 0):

		query = \
			'select  ' \
			'message.ROWID as message_ROWID, '\
			'message.guid as message_guid, '\
			'message.text as message_text, '\
			'message.handle_id as message_handle_id, '\
			'message.other_handle as message_other_handle,'\
			'message.service as message_service, '\
			'message.date as message_date, '\
			'message.is_from_me as message_is_from_me, '\
			'attachment.rowid as attachment_rowid, '\
			'attachment.filename as attachment_filename, '\
			'attachment.mime_type as attachment_mime_type, '\
			'attachment.transfer_name as attachment_transfer_name, '\
			'chat_handle_join.handle_id as chat_handle_id ' \
			'from message '\
			'left OUTER JOIN message_attachment_join on message.ROWID = message_attachment_join.message_id '\
			'left OUTER join attachment on message_attachment_join.attachment_id = attachment.ROWID '\
			'left OUTER JOIN chat_message_join on message.ROWID=chat_message_join.message_id ' \
			'left OUTER JOIN chat_handle_join on chat_message_join.chat_id = chat_handle_join.chat_id ' \
			'where message.ROWID>%d ' \
			'order by message.ROWID, chat_handle_join.handle_id' % (last_processed_rowid)

		c = self.conn.cursor().execute(query)

		msg = {'rowid':-1}
		row = c.fetchone()
		while row:
			if msg['rowid'] != row['message_ROWID']:
				msg = {'rowid': row['message_ROWID'],
					   'guid': row['message_guid'],
					   'text': row['message_text'],
				 	   'handle_id': row['message_handle_id'] or row['message_other_handle'],
					   'service': row['message_service'],
					   'date': row['message_date'],
					   'is_from_me': row['message_is_from_me'],
				 	   'attachments' : [],
					   'chat_handles' : set()}
				attachments_set = set()
			if row['attachment_rowid'] and row['attachment_rowid'] not in attachments_set\
					and row['attachment_filename']:
				filename = row['attachment_filename'].replace('~', self.user_dir)
				if self.path != self.config_path:
					filename = self.path + filename[-len(filename)+len(self.config_path):]
				if os.path.exists(filename):
					msg['attachments'].append({'filename': filename,
										   'mime_type':row['attachment_mime_type'],
										   'transfer_name':row['attachment_transfer_name']})
				attachments_set.add(row['attachment_rowid'])
			if row['chat_handle_id']:
				msg['chat_handles'].add(row['chat_handle_id'])
			row = c.fetchone()
			if not row or msg['rowid'] != row['message_ROWID']:
				if msg['handle_id'] != 0:
					msg['chat_handles'].add(msg['handle_id'])
				yield msg
