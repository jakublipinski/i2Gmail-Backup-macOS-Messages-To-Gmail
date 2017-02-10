import os
import sqlite3

class MessagesDB:


	def __init__(self, path = ''):
		user_dir = os.path.expanduser('~')
		self.conn = sqlite3.connect(user_dir + path + '/chat.db')

	def get_handles(self):
		for row in self.conn.cursor().execute('select ROWID, id from handle'):
			yield {'rowid':row[0], 'id':row[1]}

	def get_messages(self, last_processed_rowid = 0):
		for row in self.conn.cursor().execute(
				'select ROWID, guid, text, handle_id, service, date, is_from_me ' \
				'from message '\
				'where ROWID>? and handle_id>0 '\
				'order by ROWID',(last_processed_rowid,)):
			yield {'rowid':row[0], 'guid':row[1], 'text':row[2], 'handle_id':row[3],
				   'service':row[4], 'date':row[5], 'is_from_me':row[6]}
