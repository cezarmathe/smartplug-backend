
import pymysql

import json

class Database():

    def __init__(self):

        with open('constants/database.secret.json', 'r') as f:
            creds = json.loads(f.read())

        self.db = pymysql.connect(creds['host'], creds['username'], creds['password'], creds['db_name'])

        self.cursor = self.db.cursor()

    def show_db(self):
        self.cursor.execute('SHOW DATABASES;')
        return self.cursor.fetch()
