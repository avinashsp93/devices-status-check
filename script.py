import requests
 
url = 'https://api.spaceagelabs.com.sg/admin/login/?next=/admin/'
client = requests.session()
# Retrieve the CSRF token first
csrf = client.get(url).cookies['csrftoken']

print(csrf)

login_data = dict(username='saladmin', password='Space@GE;labs', csrfmiddlewaretoken=csrf, next='/')
r = client.post(url, data=login_data, headers=dict(Referer=url))
 
# Check if it worked?
print(r.text)