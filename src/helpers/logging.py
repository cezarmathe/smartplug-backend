
import logzero
from logzero import logger

logzero.logfile('logs/latest.log')

class Logger():

    def __init__(self):
        return

    def logFlask(self, text):
        logger.info("[FLASK] -- " + text)

    def logMQTT(self, text):
        logger.info("[MQTT] -- " + text)

    def logMQTTMsg(self, text):
        logger.info("[MQTT Msg Handler] -- " + text)

    def logRouting(self, text):
        logger.info("[HTTP Route] -- " + text)

    def logInfo(self, text):
        logger.info("[INFO] -- " + text)
