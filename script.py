import requests
import json
import csv
import datetime

def printable_date_format(date_object):
    date_string = datetime.datetime.strptime(date_object[0:date_object.index('.')], '%Y-%m-%dT%H:%M:%S').strftime("%A, %B %d, %Y %I:%M:%S")
    return date_string

def check_date_intervals(date_object):
    number_of_seconds = (datetime.datetime.now() - datetime.datetime.strptime(date_object[0:date_object.index('.')], '%Y-%m-%dT%H:%M:%S')).total_seconds()
    if(number_of_seconds < 86400):
        return True
    else:
        return False

# Establishing connection
url = 'https://api.spaceagelabs.com.sg/admin/login/?next=/admin/'
client = requests.session()
# Retrieve the CSRF token first
csrf = client.get(url).cookies['csrftoken']
login_data = dict(username='saladmin', password='Space@GE;labs', csrfmiddlewaretoken=csrf, next='/')
r = client.post(url, data=login_data, headers=dict(Referer=url))

# Create and open an output file pointer, close it at the end
out_fp = open("output.json", "w")

# GET request for Devices
r = client.get("https://api.spaceagelabs.com.sg/v2/Spaceagelabs/devices?limit=100&offset=0")

out_fp.write(r.text)
results = json.loads(r.text)['results']
count = json.loads(r.text)['count']
with open('status.csv', 'w', newline='') as f:
    thewriter = csv.writer(f)

    thewriter.writerow(['Devices Count', count])
    thewriter.writerow('\n')

    thewriter.writerow(['Device ID', 'Name', 'Status', 'Last Seen'])
    for i in results:
        dt = 'Not Known'
        if(i['last_seen'] != None):
            dt = datetime.datetime.fromtimestamp(i['last_seen']).strftime("%A, %B %d, %Y %I:%M:%S")
        status = 'Inactive'
        if(i['is_active']):
            status = 'Active'
        thewriter.writerow([i['id'], i['device_name'], status, dt])
    thewriter.writerow('\n')
    
# GET request for Devices Alarms
r = client.get("https://api.spaceagelabs.com.sg/v2/Spaceagelabs/devices-alarms?limit=100&offset=0")

out_fp.write(r.text)
results = json.loads(r.text)['results']
count = json.loads(r.text)['count']
with open('status.csv', 'a', newline='') as f:
    thewriter = csv.writer(f)

    thewriter.writerow(['Devices Alarms Count', count])
    thewriter.writerow('\n')

    thewriter.writerow(['Device ID', 'Created At', 'Cleared At'])
    for i in results:
        # Javascript date parsed into known format first and then formatted in accordance with the output requirement
        date_cleared = i['cleared']
        date_created = printable_date_format(i['created_at'])
        if(date_cleared):
            date_cleared = printable_date_format(i['cleared_at'])
        else:
            date_cleared = 'Not Known'
        if(check_date_intervals(i['created_at'])):
            thewriter.writerow([i['id'], date_created, date_cleared])
    thewriter.writerow('\n')
    

r = client.get("https://api.spaceagelabs.com.sg/v2/Spaceagelabs/feeds/alarms/?limit=100&offset=0")

out_fp.write(r.text)
results = json.loads(r.text)['results']
count = json.loads(r.text)['count']
with open('status.csv', 'a', newline='') as f:
    thewriter = csv.writer(f)

    thewriter.writerow(['Feed Alarms Count', count])
    thewriter.writerow('\n')

    thewriter.writerow(['Device ID', 'Created At', 'Cleared At'])
    for i in results:
        # Javascript date parsed into known format first and then formatted in accordance with the output requirement
        date_cleared = i['cleared']
        date_created = printable_date_format(i['created_at'])
        
        if(date_cleared):
            date_cleared = printable_date_format(i['cleared_at'])
        else:
            date_cleared = 'Not Known'
        if(check_date_intervals(i['created_at'])):
            thewriter.writerow([i['id'], date_created, date_cleared])
    thewriter.writerow('\n')

out_fp.close()



results = []
results = json.loads(r.text)


