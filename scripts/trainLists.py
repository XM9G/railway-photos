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


def getTramSets(tram):
    result = []
    fieldnames = ['Tram', 'Operator', 'Unused', 'Livery', 'Status', 'Interior', 'In Service', 'Withdrawn', 'Notes']

    with open('tramsets.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        next(reader)
        for row in reader:
            tram_id = row['Tram'].split('.')[0]
            if tram_id == tram:
                scrapped = row['Status'].strip().lower() == 'scrapped'
                result.append({'tram': row['Tram'].split('.')[1], 'scrapped': scrapped})
    return result