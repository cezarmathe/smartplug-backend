import json

def retrieve(secret):
    with open('constants/' + secret + '.secret.json', 'r') as f:
        creds = json.loads(f.read())
    return creds
