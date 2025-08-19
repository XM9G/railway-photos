import os
import sqlite3
from tabnanny import check
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, send_file, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


from scripts.cloudinaryAPI import getSmallerSize
from scripts.databaseManager import addPhoto, getPhotoUrls, getPhotos, siteStats
from scripts.trainLists import getSets, getTramSets

app = Flask(__name__)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["1000 per hour"]
)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def mainPage():
    if request.args: # if theres url params from the search
        return redirect(url_for('advSearch', **request.args))
    
    allPhotos = getPhotos()
    tramPhotos = getPhotos(mode='tram')
    withImage = []
    

    for photo in allPhotos + tramPhotos:
        for car in photo[1].split('-'):
            car = car.strip().upper()
            withImage.append(car)

    # Get train sets
    comeng = getSets('EDI Comeng') + getSets('Alstom Comeng')
    xtrap100 = getSets("X'Trapolis 100")
    siemens = getSets('Siemens Nexas')
    hcmt = getSets('HCMT')
    xtrap2 = getSets("X'Trapolis 2.0")
    vlocity = getSets('Vlocity')
    sprinter = getSets('Sprinter')
    ncl = getSets('N Class')
    
    # tram sets
    z = getTramSets('Z3')
    a = getTramSets('A1') + getTramSets('A2')
    b = getTramSets('B2')
    c1 = getTramSets('C')
    c2 = getTramSets('C2')
    d = getTramSets('D1') + getTramSets('D2')
    e = getTramSets('E') + getTramSets('E2')
    w = getTramSets('W8')
    
    metroAndVLine = comeng + xtrap100 + siemens + hcmt + xtrap2 + vlocity + sprinter+ ncl

    for train in metroAndVLine:
        if isinstance(train['cars'], str):
            train['cars'] = train['cars'].split('-')
        elif isinstance(train['cars'], list) and len(train['cars']) == 1 and '-' in train['cars'][0]:
            train['cars'] = train['cars'][0].split('-')
        
    # other trains
    otherTrains = []
    for photo in allPhotos:
        if photo[2] not in ['Alstom Comeng', 'EDI Comeng', "X'Trapolis 100", "X'Trapolis 2.0", 'Siemens Nexas', 'HCMT', 'Sprinter', 'VLocity', 'N Class']:
            otherTrains.append([photo[1], photo[2]])
            
    # statistics
    stats = siteStats()
    
    return render_template('index.html', comeng_trains=comeng, xtrap100_trains=xtrap100, siemens_trains=siemens, hcmt_trains=hcmt, xtrap2_trains=xtrap2, vlocity_trains=vlocity, sprinter_trains=sprinter, ncl_trains = ncl, otherTrains=otherTrains, linkedNumbers=withImage, stats=stats,Zclass=z,Aclass=a,Bclass=b,C1class=c1,C2class=c2,Dclass=d,Eclass=e,Wclass=w)



# Train image page
@app.route('/trains/<number>')
def train_page(number):
    photos = getPhotos(number=number)
    
    if len(photos) == 0:
        return render_template('noresults.html', number=number)
    
    photosInfo = []
    for photo in photos:
        if photo[6] == 1:
            photosInfo.insert(0, {
                'number': photo[1],
                'type': photo[2],
                'date': photo[3],
                'location': photo[4],
                'photographer': photo[5],
                'url': getSmallerSize(photo[7], 1000, best=True),
                'featured': photo[6],
                'note': photo[8],
                'id': photo[0],
                'mode': 'train',
            })
        else:
            photosInfo.append ({
                'number': photo[1],
                'type': photo[2],
                'date': photo[3],
                'location': photo[4],
                'photographer': photo[5],
                'url': getSmallerSize(photo[7], 1000, best=True),
                'featured': photo[6],
                'note': photo[8],
                'id': photo[0],
                'mode': 'train',
            })
    return render_template('photopage.html', info=photosInfo)

@app.route('/trams/<number>')
def tram_page(number):
    photos = getPhotos(number=number, mode='tram')
    
    if len(photos) == 0:
        return render_template('noresults.html', number=number)
    
    photosInfo = []
    for photo in photos:
        if photo[6] == 1:
            photosInfo.insert(0, {
                'number': photo[1],
                'type': photo[2],
                'date': photo[3],
                'location': photo[4],
                'photographer': photo[5],
                'url': getSmallerSize(photo[7], 1000, best=True),
                'featured': photo[6],
                'note': photo[8],
                'id': photo[0],
                'mode': 'tram',
            })
        else:
            photosInfo.append({
                'number': photo[1],
                'type': photo[2],
                'date': photo[3],
                'location': photo[4],
                'photographer': photo[5],
                'url': getSmallerSize(photo[7], 1000, best=True),
                'featured': photo[6],
                'note': photo[8],
                'id': photo[0],
                'mode': 'tram'
            })
    return render_template('photopage.html', info=photosInfo)

# Redirect from the old URL format
@app.route('/trains/<path:subpath>/<train_number>')
def redirect_train(subpath, train_number):
    train_number = train_number.strip('.html')
    return redirect(url_for('train_page', number=train_number), code=301)

# advanced search
@app.route('/search')
def advSearch():
    if not request.args:
     return render_template('search.html')
    else:
        number = request.args.get('number', None)
        trainType = request.args.get('type', None)
        date = request.args.get('date', None)
        location = request.args.get('location', None)
        photographer = request.args.get('photographer', None)
        if request.args.get('featured', None) == 'featured':
            featured = 1
        else:
            featured = None
        
        photos = getPhotos(number=number, type=trainType, date=date, location=location, photographer=photographer, featured=featured)
        trains = []
        for photo in photos:
            trains.append ({
                'number': photo[1],
                'type': photo[2],
                'date': photo[3],
                'location': photo[4],
                'photographer': photo[5],
                'url': getSmallerSize(photo[7], 500),
                'featured': photo[6],
                'note': photo[8],
                'id': photo[0],
                'mode': 'train',
            })
        trains.sort(key=lambda x: x['date'], reverse=True) # this thing sorts by the date 
        lenght = len(trains)
        return render_template('searchresults.html', trains=trains, length=lenght)
        
    
# view counter
@app.route('/api/view/<photoID>/<mode>')
@limiter.limit("1000 per hour")
def count_view(photoID, mode):
    try:
        conn = sqlite3.connect('databases/trains.db')
        cursor = conn.cursor()
        
        if mode == 'train':
            tableName = 'views'
        elif mode == 'tram':
            tableName = 'tramviews'
        
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {tableName} (
                id TEXT PRIMARY KEY,
                views INTEGER
            )
        ''')
        cursor.execute(f'SELECT views FROM {tableName} WHERE id = ?', (photoID,))
        result = cursor.fetchone()
    
        if result:
            new_views = result[0] + 1
            cursor.execute(f'UPDATE {tableName} SET views = ? WHERE id = ?', (new_views, photoID))
        else:
            cursor.execute(f'INSERT INTO {tableName} (id, views) VALUES (?, 1)', (photoID,))
        
        conn.commit()
        cursor.execute(f'SELECT views FROM {tableName} WHERE id = ?', (photoID,))
        current = cursor.fetchone()
        current_views = current[0] if current else 0

        return {'photoID': photoID, 'views': current_views}, 200
        
    except Exception as e:
        return {'error': str(e)}, 500
    
    finally:
        conn.close()
        
# temp redirect for station photos
@app.route('/stations/melbourne/<station>')
def station(station):
    return render_template('stationTempPage.html')

@app.route('/lines/<line>')
def line(line):
    return render_template('lineTempPage.html')

# image URLS for discord bot
@app.route('/api/photos/<path:filename>')
def photo_url(filename):

    urlsList = getPhotoUrls(filename, optimise=True)
    if len(urlsList) == 0:
        return jsonify({"error": "No photos found"}), 404
    else:
        return jsonify({"photos": urlsList})

# trainsets CSV download
@app.route('/api/trainsets.csv')
def trainsetsCSV():
    return send_file('trainsets.csv', as_attachment=True, download_name='trainsets.csv', mimetype='text/csv')

# image adder api
@app.route('/api/upload', methods=['POST'])
def upload_image():
    # Check auth
    def check_auth():
        load_dotenv()
        auth_header = request.headers.get('Authorization')
        token = auth_header
        print(f"Received token: {token}")
        print(f"Expected token: {os.getenv('API_TOKEN')}")
        return token == os.getenv('API_TOKEN')
    
    if not check_auth():
        return jsonify({'error': 'Unauthorized access'}), 401

    try:
        # Check if image is provided
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        file = request.files['image']

        # Validate file extension
        if not file.filename.endswith('.webp'):
            return jsonify({'error': 'Only .webp images are allowed'}), 400

        # Get form data directly
        number = request.form.get('number', 'Unknown')
        trainType = request.form.get('type', 'Unknown')
        location = request.form.get('location', 'Unknown')
        date = request.form.get('date', 'Unknown')
        photographer = request.form.get('photographer', 'Unknown')
        featured = request.form.get('featured', 'N')
        note = request.form.get('note', '')
        mode = request.form.get('mode','train')

        if not number or not trainType or not location:
            return jsonify({'error': f'Missing required form fields'}), 400

        # Save the file
        filename = f'{number}-{photographer}-{file.filename}'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            from scripts.cloudinaryAPI import uploadImage
            image_url = uploadImage(file_path, filename)
            if featured.lower() == 'y':
                featured = True
            else:
                featured = False
            addPhoto(number, trainType, date, location, photographer, featured, image_url, note, mode)
            
        except Exception as e:
            return jsonify({'error': f'Failed to upload image: {str(e)}'}), 500

        response = {
            'message': f'Image {filename} uploaded successfully!',
            'url': image_url,
            'number': number,
            'type': trainType,
            'date': date,
            'location': location,
            'photographer': photographer,
            'featured': featured,
            'note': note,
            'mode': mode,
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
        


if __name__ == '__main__':
    app.run(debug=True, port=6966)