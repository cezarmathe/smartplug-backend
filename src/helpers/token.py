
import jwt

class TokenUtility():

    def __init__(self):
        return

    def set_signature(self, signature):
        self.signature = signature

    def createToken(self, email):
        return jwt.ecnode({'email' : email}, self.signature, algorithm='HS256')

    def decodeToken(self, token):
        return jwt.decode(token, self.signature, algorithm='HS256')
