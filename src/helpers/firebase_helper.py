from pyfcm import FCMNotification
import helpers.secret_parser as secret

secrets = secret.retrieve('firebase')

push_service = FCMNotification(api_key=secrets["server-key"])

registration_id = secrets["sender-id"]
message_title = "Uber update"
message_body = "Hi john, your customized news for today is ready"
result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

def print_result():
    print(result)
