import csv

with open('mycsv.csv', 'w', newline='') as f:
    thewriter = csv.writer(f)

    thewriter.writerow(['Username', 'Password'])
    thewriter.writerow(['demo@spaceagelabs.com.sg','demo1234'])