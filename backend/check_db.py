import os

import mysql.connector


CONFIG = {
    'host': os.environ.get('MYSQL_HOST', '127.0.0.1'),
    'port': int(os.environ.get('MYSQL_PORT', 3306)),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', ''),
    'database': os.environ.get('MYSQL_DATABASE', 'app_db'),
}

conn = mysql.connector.connect(**CONFIG)
cur = conn.cursor()
cur.execute("SHOW TABLES")
print('tables:', cur.fetchall())
cur.close()
conn.close()
