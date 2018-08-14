
import logzero
from logzero import logger

logzero.logfile('logs/latest.log')

class Logger():

    def __init__(self):
        return

    def setTag(self, tag):
        self.tag = tag

    def logFlask(self, text):
        logger.info("[FLASK] -- " + text)

    def logMQTT(self, text):
        logger.info("[MQTT] -- " + text)

    def logMQTTMsg(self, text):
        logger.info("[MQTT Msg Handler] -- " + text)

    def logRouting(self, endpoint, method, text):
        logger.info("[HTTP Route] endpoint: " + endpoint + "; method: " + method + " -- " + text)

    def logInfo(self, text):
        logger.info("[INFO] -- " + text)

    def logTag(self, text):
        logger.info("[" + self.tag + "] -- " + text)
