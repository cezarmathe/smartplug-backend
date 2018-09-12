
import pymysql
import pymysql.cursors

import json
import os

class Database():

    def __init__(self, tokens, logger):
        # with open('constants/database.secret.json', 'r') as f:
            # self.creds = json.loads(f.read())
        self.tokens = tokens
        self.tokens.logger.setTag("TokenUtility")
        self.logger = logger
        self.logger.setTag("Database")


    def connect(self):
        self.connection = pymysql.connect(os.environ['DB_HOST'], os.environ['DB_USER'], os.environ['DB_PASS'], os.environ['DB_NAME'])
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


    def checkUserEmail(self, email):
        self.connect()

        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM user WHERE email=\'%s\'"
            cursor.execute(sql % (email))
            self.logger.logTag("executed sql script")

            if (cursor.rowcount != 0):
                result = cursor.fetchall()
            else:
                result = None

        return result


    def getUserFromToken(self, token):
        self.connect()

        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM user WHERE token=\'%s\'"
            cursor.execute(sql % (token))
            self.logger.logTag("executed sql script")

            if (cursor.rowcount != 0):
                result = cursor.fetchall()
            else:
                result = None

        return result
    # END USER

    # DEVICE
    def getDeviceList(self, id):
        self.connect()
        with self.connection.cursor() as cursor:
            sql = "SELECT device_id FROM user_has_device WHERE user_id=\'%s\'"
            print(id)
            cursor.execute(sql % id)
            dev_id_list = cursor.fetchall()
            # print(dev_id_list)

            sql = "SELECT id,is_online,name,status FROM device WHERE `id` IN ("
            for i in dev_id_list:
                # print(str(i))
                sql += str(i[0]) + ", "
            sql += "-1)"
            print(sql)
            cursor.execute(sql)
            # print(sql)
            return cursor.fetchall()

    def createDevice(self, name, user_id):
        self.connect()

        with self.connection.cursor() as cursor:
            sql = "INSERT INTO `device` (`name`,`is_online`,`status`,`user_id`) VALUES (\'%s\', \'%i\', \'%i\', \'%s\')"
            cursor.execute(sql % (name, 0, 0, user_id))

            self.connection.commit()

            sql = "SELECT LAST_INSERT_ID()"
            cursor.execute(sql)

            self.disconnect()

            dev_id = cursor.fetchone()

            self.addDeviceUserPair(dev_id[0], user_id)

            return dev_id[0]


    def updateDeviceStatus(self, id, status):
        self.logger.logTag("update device status")

        self.connect()

        # self.logger.logTag("id:" + str(id) + "/status:" + str(status))

        with self.connection.cursor() as cursor:
            sql = "UPDATE `device` SET status=\'%i\' WHERE id=\'%i\'"
            cursor.execute(sql % (int(status), int(id)))

            self.connection.commit()

        self.disconnect()



    def checkDeviceOwnership(self, device_id, user_id):
        self.connect()

        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM device WHERE user_id=\'%s\' AND id=\'%s\'"
            cursor.execute(sql % (user_id, device_id))
            self.logger.logTag("executed sql script")

            if (cursor.rowcount != 0):
                return True
            else:
                return False


    def checkDevicePermission(self, device_id, user_id):
        # todo
        return

    def addDeviceUserPair(self, device_id, user_id):
        self.connect()

        with self.connection.cursor() as cursor:
            sql = "INSERT INTO `user_has_device` (`user_id`,`device_id`) VALUES (\'%s\',\'%s\')"
            cursor.execute(sql % (user_id, device_id))

            self.connection.commit()
        self.disconnect()
        return

    # END DEVICE

    # todo other functions
