
import pymysql
import pymysql.cursors

import json

class Database():

    def __init__(self, tokens, logger):
        with open('constants/database.secret.json', 'r') as f:
            self.creds = json.loads(f.read())
            self.tokens = tokens
            self.tokens.logger.setTag("TokenUtility")
            self.logger = logger
            self.logger.setTag("Database")


    def connect(self):
        self.connection = pymysql.connect(self.creds['host'], self.creds['username'], self.creds['password'], self.creds['db_name'])
        self.logger.logTag("connected to database")


    def disconnect(self):
        self.connection.close()
        self.logger.logTag("disconnected from database")


    # USER
    def createUser(self, email, password):
        self.connect()

        tk = self.tokens.createToken(email)

        with self.connection.cursor() as cursor:
            sql = "INSERT INTO `user` (`email`, `password`, `has_premium`, `has_paid`, `token`) VALUES (%s, %s, 0, 0, %s)"
            cursor.execute(sql, (email, password, tk))
            self.logger.logTag("executed sql script")

        self.connection.commit()
        self.logger.logTag("commit")
        self.disconnect()

        return tk


    def checkUser(self, email, password, conflict):
        self.connect()

        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM user WHERE email=\'%s\'"
            cursor.execute(sql % email)
            self.logger.logTag("executed sql script")

            result1 = int(cursor.rowcount)
            # print("result1=" + str(cursor.rowcount))

        if (conflict):
            if (result1 != 0):
                return False
        else:
            if (result1 == 0):
                return False

        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM user WHERE email=\'%s\' AND password=\'%s\'"
            cursor.execute(sql % (email, password))
            self.logger.logTag("executed sql script")

            result2 = int(cursor.rowcount)
            # print("result2=" + str(cursor.rowcount))

            user = cursor.fetchone()

        self.disconnect()

        if (conflict):
            if (result2 != 0):
                return False
        else:
            if (result2 == 0):
                return False

        if (conflict):
            return True
        return user


    def getUserFromToken(self, token):
        self.connect()

        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM user WHERE token=\'%s\'"
            cursor.execute(sql % token)
            self.logger.logTag("executed sql script")

            if (cursor.rowcount != 0):
                result = cursor.fetchone()
            else:
                result = None

        return result
    # END USER

    # DEVICE
    def getDeviceList(self, id):
        self.connect()

        with self.connection.cursor() as cursor:
            sql = "SELECT id,name,is_online,status FROM device WHERE user_id=\'%i\'"
            cursor.execute(sql % id)
            return cursor.fetchall()

    def createDevice(self, name, user_id):
        self.connect()

        with self.connection.cursor() as cursor:
            sql = "INSERT INTO device(`name`, `is_online`, `status`, `user_id`) VALUES (%s, %i, %i, %i)"
            cursor.execute(sql % (name, 0, 0, user_id))

            self.connection.commit()

            sql = "SELECT LAST_INSERT_ID()"
            cursor.execute(sql)

            return cursor.fetchone()

    def checkDeviceOwnership(self, device_id, user_id):
        # todo
        return

    def checkDevicePermission(self, device_id, user_id):
        # todo
        return

    def updateDeviceStatus(self, device_id, status):
        # todo
        return

    # END DEVICE

    # todo other functions
