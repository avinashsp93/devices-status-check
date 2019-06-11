import requests
import json

payload = {"username": "demo@spaceagelabs.com.sg", "password": "demo1234"}
r = requests.post("https://api.spaceagelabs.com.sg/v2/login", data=payload)
out = json.loads(r.content.decode('utf-8'))

head = {'Authorization': 'token {}'.format(out['token'])}
response = requests.get("https://reye.spaceagelabs.com.sg/#/login", headers = head)
print(response.text)