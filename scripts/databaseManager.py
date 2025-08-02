import os
import sqlite3

from httpx import get
from numpy import add

def addPhoto(number, type, date, location, photographer, featured:bool, url):
    conn = sqlite3.connect('databases/trains.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS photos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT NOT NULL,
        type TEXT NOT NULL,
        date TEXT NOT NULL,
        location TEXT NOT NULL,
        photographer TEXT NOT NULL,
        featured BOOLEAN NOT NULL DEFAULT 0,
        url TEXT NOT NULL
    )''')
    cursor.execute('''
    INSERT INTO photos (number, type, date, location, photographer, featured, url)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (number, type, date, location, photographer, featured, url))
    
    conn.commit()
    conn.close()
    
def getPhotos(number=None, type=None, date=None, location=None, photographer=None, featured=None):
    conn = sqlite3.connect('databases/trains.db')
    cursor = conn.cursor()
    
    query = 'SELECT * FROM photos WHERE 1=1'
    params = []
    
    if number:
        query += ' AND number=?'
        params.append(number)
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
    
    cursor.execute(query, params)
    photos = cursor.fetchall()
    
    conn.close()
    return photos

addPhoto(
    number='XM9G',
    type='X\'Trapolis 100',
    date='2025-10-31',
    location='Tarrawrra',
    photographer='Clyde',
    featured=False,
    url='https://res.cloudinary.com/dwfrb2wpw/image/upload/v1754123478/P16_ly7xq3.webp')