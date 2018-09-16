
import json


def serializeDeviceList(list):
    print(list)
    device_list = {'list' : []}
    dl = device_list['list']
    for i in list:
        # print(i)
        device_data = {}
        device_data['id'] = i[0]
        device_data['name'] = i[1]
        if (i[2] == 0):
            device_data['isOnline'] = False
        else:
            device_data['isOnline'] = True
        if (i[3] == 0):
            device_data['status'] = False
        else:
            device_data['status'] = True
        dl.append(device_data)
        device_list['list'] = dl
    print(dl)
    return device_list
