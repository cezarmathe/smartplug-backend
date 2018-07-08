import requests

x = input()
r = requests.post("http://78.96.238.161:1234/upstream", data={"status": x})

print(r.status_code, r.reason)
print(r.text[:300] + '...')
