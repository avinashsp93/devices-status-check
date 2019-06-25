import csv

with open('contacts.csv', 'w', newline='') as f:
    thewriter = csv.writer(f)

    thewriter.writerow(['avinashsp93@gmail.com'])
    thewriter.writerow(['deepthidesaitwinkle@gmail.com'])