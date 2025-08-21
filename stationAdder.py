from scripts.databaseManager import addStationPhoto


while True:
    station = input('Station: ')
    photographer = input('Photographer: ')
    featured = input('Featured (Y/N): ')
    url = input('Image URL: ')
    date = input('Date (YYYY-MM-DD): ')
    note = input('Note (optional): ')
    featured = True if featured.lower() == 'y' else False
    addStationPhoto(station, photographer,date,url, featured, note)
    print(f'Photo added successfully! {station} - {photographer} - {featured} - {url} - {note}')