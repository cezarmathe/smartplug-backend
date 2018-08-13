
import pymysql
import pymysql.cursors

import json

class Database():

    def __init__(self):
        with open('constants/database.secret.json', 'r') as f:
            self.creds = json.loads(f.read())


    def connect(self):
        self.connection = pymysql.connect(self.creds['host'], self.creds['username'], self.creds['password'], self.creds['db_name'])


    def disconnect(self):
        self.connection.close()


    def addUser(self, email, password):
        self.connect()

        with self.connection.cursor() as cursor:
            sql = "INSERT INTO `user` (`email`, `password`, `has_premium`, `has_paid`) VALUES (%s, %s, 0, 0, 'token')"
            cursor.execute(sql, (email, password))

        self.connection.commit()
        self.disconnect()

        return True


    def checkUser(self, email, password):
        self.connect()

        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM `user` WHERE email =  \'" + email + "\' AND password = \'" + password + "\'"
            cursor.execute(sql)

            if (cursor.rowcount > 0):
                return True
            return False
    # todo other functions
