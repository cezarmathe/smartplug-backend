import helpers.firebase_helper as fb
import helpers.mqtt_helper as mqtt

fb.print_result()

mqtt.mqqt_connect()
mqtt.client.loop_forever()
