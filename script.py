import requests
import json
import csv
import datetime

url = 'https://api.spaceagelabs.com.sg/admin/login/?next=/admin/'
client = requests.session()
# Retrieve the CSRF token first
csrf = client.get(url).cookies['csrftoken']

login_data = dict(username='saladmin', password='Space@GE;labs', csrfmiddlewaretoken=csrf, next='/')
r = client.post(url, data=login_data, headers=dict(Referer=url))
r = client.get("https://api.spaceagelabs.com.sg/v2/Spaceagelabs/devices?limit=100&offset=0")

out_fp = open("output.json", "w")
out_fp.write(r.text)
results = json.loads(r.text)['results']
with open('status.csv', 'w', newline='') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(['Device ID', 'Name', 'Status', 'Last Seen'])
    for i in results:
        dt = 'Not Known'
        if(i['last_seen'] != None):
            dt = datetime.datetime.fromtimestamp(i['last_seen']).strftime("%A, %B %d, %Y %I:%M:%S")
        status = 'Inactive'
        if(i['is_active']):
            status = 'Active'
        thewriter.writerow([i['device_id'], i['device_name'], status, dt])
        
out_fp.close()

results = []
results = json.loads(r.text)


