from databaseManager import addPhoto


while True:
    number = input('Number: ')
    ttype = input('Type: ')
    date = input('Date (YYYY-MM-DD): ')
    location = input('Location: ')
    photographer = input('Photographer: ')
    featured = input('Featured (Y/N): ')
    url = input('Image URL: ')
    note = input('Note (optional): ')
    featured = True if featured.lower() == 'y' else False
    addPhoto(number, ttype, date, location, photographer, featured, url, note)
    print(f'Photo added successfully! {number} - {ttype} - {date} - {location} - {photographer} - {featured} - {url} - {note}')