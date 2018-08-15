
import json


def serializeDeviceList(list):
    print(list)
    device_list = {'list' : []}
    dl = device_list['list']
    for i in list:
        print(i)
        device_data = {}
        device_data['id'] = i[0]
        device_data['name'] = i[1]
        device_data['status'] = i[2]
        device_data['isOnline'] = i[3]
        dl.append(device_data)
        device_list['list'] = dl
    return device_list
