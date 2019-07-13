import requests
import json
import csv
import datetime
import smtplib
import base64

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from string import Template

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

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


with open('organizations.csv') as org_file:
    org_reader = csv.reader(org_file, delimiter=',')
    count = 0
    for row in org_reader:
        print(row[0])
        # GET request for Devices
        r = client.get("https://api.spaceagelabs.com.sg/v2/"+row[0]+"/devices?limit=100&offset=0")

        # Create and open an output file pointer, close it at the end
        out_fp = open("output.json", "w", encoding="utf-8")

        out_fp.write(r.text)
        results = json.loads(r.text)['results']
        count = json.loads(r.text)['count']
        write_append_flag = 'w'
        if(count > 0):
            write_append_flag = 'a'
        count+=1
        
        with open('status.csv', write_append_flag , newline='') as f:
            thewriter = csv.writer(f)

            thewriter.writerow(['Organization Name', row[0]])
            thewriter.writerow('\n')

            thewriter.writerow(['Devices'])
            thewriter.writerow(['Name', 'Alias', 'Status', 'Last Seen'])
            active_count = 0
            total_count = 0
            for i in results:
                total_count+=1
                dt = 'Not Known'
                if(i['last_seen'] != None):
                    dt = datetime.datetime.fromtimestamp(i['last_seen']).strftime("%A, %B %d, %Y %I:%M:%S")
                status = 'Inactive'
                if(i['is_active']):
                    status = 'Active'
                    active_count+=1
                thewriter.writerow([i['device_name'], i['alias_name'].encode("utf-8"), status, dt])
            thewriter.writerow('\n')
            device_health = 'Unknown'
            if(total_count != 0):
                device_health = ((active_count*1.0)/total_count)*100
            thewriter.writerow(['Devices Health of Organization', device_health])
            thewriter.writerow('\n')
            
        # GET request for Devices Alarms
        r = client.get("https://api.spaceagelabs.com.sg/v2/"+row[0]+"/devices-alarms?limit=100&offset=0")

        out_fp.write(r.text)
        results = json.loads(r.text)['results']
        count = json.loads(r.text)['count']
        with open('status.csv', 'a', newline='') as f:
            thewriter = csv.writer(f)

            thewriter.writerow(['Devices Alarms'])
            thewriter.writerow(['Device Name', 'Created At', 'Cleared At'])
            for i in results:
                # Javascript date parsed into known format first and then formatted in accordance with the output requirement
                date_cleared = i['cleared']
                date_created = printable_date_format(i['created_at'])
                if(date_cleared):
                    date_cleared = printable_date_format(i['cleared_at'])
                else:
                    date_cleared = 'Not Known'
                if(check_date_intervals(i['created_at'])):
                    thewriter.writerow([i['name'], date_created, date_cleared])
            thewriter.writerow('\n')
            

        r = client.get("https://api.spaceagelabs.com.sg/v2/"+row[0]+"/feeds/alarms/?limit=100&offset=0")

        out_fp.write(r.text)
        results = json.loads(r.text)['results']
        count = json.loads(r.text)['count']
        with open('status.csv', 'a', newline='') as f:
            thewriter = csv.writer(f)

            thewriter.writerow(['Feed Alarms'])
            thewriter.writerow(['Device Name', 'Created At', 'Cleared At'])
            for i in results:
                # Javascript date parsed into known format first and then formatted in accordance with the output requirement
                date_cleared = i['cleared']
                date_created = printable_date_format(i['created_at'])
                
                if(date_cleared):
                    date_cleared = printable_date_format(i['cleared_at'])
                else:
                    date_cleared = 'Not Known'
                if(check_date_intervals(i['created_at'])):
                    thewriter.writerow([i['feed']['device']['device_name'], date_created, date_cleared])
            thewriter.writerow('\n')
        
            thewriter.writerow('\n')
            thewriter.writerow('\n')
            thewriter.writerow('\n')
            thewriter.writerow('\n')
        
        out_fp.close()

s = smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()
s.login('spaceagelabstest@gmail.com', 'sal@12345') # email id and password of the sender mail to be typed inside the single quotations respectively

with open('contacts.csv', newline='') as csvfile:

    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    # Loop through the message recepients, put all the recepients list in contacts.csv
    for row in reader:
        msg = MIMEMultipart()

        msg['From'] = 'spaceagelabstest@gmail.com' # Add email address that sends out the report
        msg['To'] = row[0] # Recepients
        msg['Subject'] = 'Device Status Results'

        message_template = read_template('message.txt')
        message = message_template.substitute('name.title()')
        msg.attach(MIMEText(message, 'plain'))

        file_attachment = open('status.csv', 'rb')
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(file_attachment.read())
        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename=status.csv")

        msg.attach(p)

        # s.send_message(msg)

        print("Mail sent successfully to " + row[0])

        del msg