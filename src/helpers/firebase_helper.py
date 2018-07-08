from pyfcm import FCMNotification
import helpers.secret_parser as secret

# Retrieve the creds
secrets = secret.retrieve('firebase')

# Create the message service
messageService = FCMNotification(api_key=secrets["server-key"])

# Simple send data to id/ids function
def sendData(id, payload, singleDevice = True):
    if singleDevice:
        result = messageService.single_device_data_message(registration_id=id, data_message=data_message)
        print("[FIREBASE]--Sent data to single device:" + result)
        return
    result = messageService.multiple_devices_data_message(registration_ids=id, data_message=data_message)
    print("[FIREBASE]--Sent data to multiple devices:" + result)
    return

# Simple send notification to id/ids function
def sendNotification(id, title, body, singleDevice = True):
    if singleDevice:
        result = messageService.notify_single_device(registration_id=id, message_title=title, message_body=body)
        print("[FIREBASE]--Sent notification to single device:" + result)
        return
    result = messageService.notifi_multiple_devices(registration_ids=id, message_title=title, message_body=body)
    print("[FIREBASE]--Sent notification to multiple devices:" + result)
    return

def cleanRegistrationIds(ids):
    return messageService.clean_registration_ids(ids)
