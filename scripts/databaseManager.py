import os
import sqlite3

from httpx import get
from numpy import add

def addPhoto(number, type, date, location, photographer, featured:bool, url, note=None):
    conn = sqlite3.connect('databases/trains.db')
    cursor = conn.cursor()
    number = number.upper()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS photos (
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
    cursor.execute('''
    INSERT INTO photos (number, type, date, location, photographer, featured, url, note)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (number, type, date, location, photographer, featured, url, note))
    
    conn.commit()
    conn.close()
    
def getPhotos(number=None, type=None, date=None, location=None, photographer=None, featured=None, note=None):
    conn = sqlite3.connect('databases/trains.db')
    cursor = conn.cursor()
    
    query = 'SELECT * FROM photos WHERE 1=1'
    params = []
    
    if number:
        query += ' AND number=?'
        params.append(number.upper())
    if type:
        query += ' AND type=?'
        params.append(type)
    if date:
        query += ' AND date=?'
        params.append(date)
    if location:
        query += ' AND location=?'
        params.append(location)
    if photographer:
        query += ' AND photographer=?'
        params.append(photographer)
    if featured is not None:
        query += ' AND featured=?'
        params.append(featured)
    if note is not None:
        query += ' AND note=?'
        params.append(note)
    
    cursor.execute(query, params)
    photos = cursor.fetchall()
    
    conn.close()
    return photos

def getPhotoUrls(number):
    conn = sqlite3.connect('databases/trains.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT url, photographer, featured FROM photos WHERE number=?', (number.upper(),))
    urls = cursor.fetchall()
    conn.close()
    if not urls:
        return []
    urlsList = []
    for url, photographer, featured in urls:

        urlsList.append({
            'url': url,
            'photographer': photographer,
            'featured': featured
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