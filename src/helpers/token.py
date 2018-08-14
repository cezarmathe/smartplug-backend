
import jwt

class TokenUtility():

    def __init__(self, logger):
        self.logger = logger
        self.logger.setTag("TokenUtility")
        return

    def set_signature(self, signature):
        self.logger.logTag("set the signature")
        self.signature = signature

    def createToken(self, email):
        self.logger.logTag("encoded a token")
        return jwt.encode({'email' : email}, self.signature, algorithm='HS256')

    def decodeToken(self, token):
        self.logger.logTag("decoded a token")
        return jwt.decode(token, self.signature, algorithm='HS256')

    def extractToken(self, request):
        self.logger.logTag("extracted a token from a request header")
        return request.headers.get('Authorization')[7:]
