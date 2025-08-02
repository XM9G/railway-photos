import csv

def getSets(train):
    result = []
    with open('trainsets.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Type'] == train:
                units = row['Set'].split(',')
                scrapped = row['Status'].lower() == 'scrapped'
                result.append({'cars': units, 'scrapped': scrapped})
    return result