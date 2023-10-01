import sqlite3

database = sqlite3.connect('project.db')

cursor = database.cursor()
#
# cursor.execute("""
#     DELETE FROM users WHERE telegram_id = ?""",(496329060,))

cursor.execute("""
DROP TABLE products""")

database.commit()
database.close()
