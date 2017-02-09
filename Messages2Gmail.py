import sqlite3
import os
import datetime

from gmail import Gmail

# q= rfc822msgid:kuku7@messages2gmail.com

if __name__ == '__main__':
	gmail = Gmail()
	gmail.connect()

	date = datetime.datetime(2015, 2, 28, 7, 45)
	msg = Gmail.create_message("<kuku7@messages2gmail.com>", "kuku", "kuku2", "kuku", date, "body")

	gmail.insert_message(msg)

#user_dir = os.path.expanduser('~')
#conn = sqlite3.connect(user_dir+'/backup_messages/chat.db')

#c = conn.cursor()

#for row in c.execute('select text from message'):
#        print row

