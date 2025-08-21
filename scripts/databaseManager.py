import os
import sqlite3

from httpx import get
from numpy import add

from scripts.cloudinaryAPI import getSmallerSize

def addPhoto(number, type, date, location, photographer, featured:bool, url, note=None, mode='train'):
    conn = sqlite3.connect('databases/trains.db')
    cursor = conn.cursor()
    number = number.upper()
    if mode.lower() == 'train':
        tableName = 'photos'
    elif mode.lower() == 'tram':
        tableName = 'tramphotos'
    
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {tableName} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT NOT NULL,
        type TEXT NOT NULL,
        date TEXT NOT NULL,
        location TEXT NOT NULL,
        photographer TEXT NOT NULL,
        featured BOOLEAN NOT NULL DEFAULT 0,
        url TEXT NOT NULL,
        note TEXT
    )''')
    cursor.execute(f'''
    INSERT INTO {tableName} (number, type, date, location, photographer, featured, url, note)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (number, type, date, location, photographer, featured, url, note))
    
    conn.commit()
    conn.close()
    
def addStationPhoto(station, photographer,date, url, featured:bool, note=None):
    conn = sqlite3.connect('databases/trains.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stationphotos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station TEXT NOT NULL,
        photographer TEXT NOT NULL,
        date TEXT NOT NULL,
        url TEXT NOT NULL,
        featured BOOLEAN NOT NULL DEFAULT 0,
        note TEXT
    )''')
    
    cursor.execute('''
    INSERT INTO stationphotos (station, photographer, date, url, featured, note)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (station, photographer, date, url, featured, note))
    
    conn.commit()
    conn.close()
    
def getPhotos(number=None, type=None, date=None, location=None, photographer=None, featured=None, note=None, mode='train', exact_match=False):
    conn = sqlite3.connect('databases/trains.db')
    cursor = conn.cursor()
    
    if mode.lower() == 'train':
        tableName = 'photos'
    elif mode.lower() == 'tram':
        tableName = 'tramphotos'
    else:
        conn.close()
        raise ValueError("Mode must be 'train' or 'tram'")
    
    query = f'SELECT * FROM {tableName} WHERE 1=1'
    params = []
    
    if number:
        query += ' AND ' + ('number=?' if exact_match else 'UPPER(number) LIKE ?')
        params.append(number.upper() if exact_match else f'%{number.upper()}%')
    if type:
        query += ' AND ' + ('type=?' if exact_match else 'UPPER(type) LIKE ?')
        params.append(type if exact_match else f'%{type.upper()}%')
    if date:
        query += ' AND date=?'
        params.append(date)
    if location:
        query += ' AND ' + ('location=?' if exact_match else 'UPPER(location) LIKE ?')
        params.append(location if exact_match else f'%{location.upper()}%')
    if photographer:
        query += ' AND ' + ('photographer=?' if exact_match else 'UPPER(photographer) LIKE ?')
        params.append(photographer if exact_match else f'%{photographer.upper()}%')
    if featured is not None:
        query += ' AND featured=?'
        params.append(featured)
    if note is not None:
        query += ' AND ' + ('note=?' if exact_match else 'UPPER(note) LIKE ?')
        params.append(note if exact_match else f'%{note.upper()}%')
            
    cursor.execute(query, params)
    photos = cursor.fetchall()
    
    conn.close()
    return photos

def getStationPhotos(station=None, photographer=None, date=None, featured=None):
    conn = sqlite3.connect('databases/trains.db')
    cursor = conn.cursor()
    
    query = 'SELECT * FROM stationphotos WHERE 1=1'
    params = []
    
    if station:
        query += ' AND station=?'
        params.append(station)
    if photographer:
        query += ' AND photographer=?'
        params.append(photographer)
    if date:
        query += ' AND date=?'
        params.append(date)
    if featured is not None:
        query += ' AND featured=?'
        params.append(featured)
    
    cursor.execute(query, params)
    photos = cursor.fetchall()
    
    conn.close()
    return photos

def getPhotoUrls(number, mode='train', optimise:bool=False):
    conn = sqlite3.connect('databases/trains.db')
    cursor = conn.cursor()
    if mode.lower() == 'train':
        tableName = 'photos'
    elif mode.lower() == 'tram':
        tableName = 'tramphotos'
    
    cursor.execute(f'SELECT url, photographer, featured, type FROM {tableName} WHERE number=?', (number.upper(),))
    urls = cursor.fetchall()
    conn.close()
    if not urls:
        return []
    urlsList = []
    for url, photographer, featured, type in urls:
        thumbnailURL = getSmallerSize(url, 200, best=False)
        if optimise:
            url = getSmallerSize(url, 1000, best=True)

        urlsList.append({
            'url': url,
            'thumbnail': thumbnailURL,
            'photographer': photographer,
            'featured': featured,
            'type': type,
        })
    return urlsList

def siteStats():
    conn = sqlite3.connect('databases/trains.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM photos')
    totalPhotos = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT number) FROM photos')
    totalTrains = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT photographer) FROM photos')
    totalPhotographers = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'totalPhotos': totalPhotos,
        'totalTrains': totalTrains,
        'totalPhotographers': totalPhotographers
    }

def getViews(photoID):
    conn = sqlite3.connect('databases/trains.db')
    cursor = conn.cursor()
    cursor.execute('SELECT views FROM views WHERE id = ?', (photoID,))
    return cursor.fetchone()[0]