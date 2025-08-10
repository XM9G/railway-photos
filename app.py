import os
import sqlite3
from tabnanny import check
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, send_file, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


from scripts.databaseManager import addPhoto, getPhotoUrls, getPhotos, siteStats
from scripts.trainLists import getSets

app = Flask(__name__)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def mainPage():
    allPhotos = getPhotos()
    withImage = []

    for photo in allPhotos:
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
    
    metroAndVLine = comeng + xtrap100 + siemens + hcmt + xtrap2 + vlocity + sprinter+ ncl

    for train in metroAndVLine:
        if isinstance(train['cars'], str):
            train['cars'] = train['cars'].split('-')
        elif isinstance(train['cars'], list) and len(train['cars']) == 1 and '-' in train['cars'][0]:
            train['cars'] = train['cars'][0].split('-')
    
    # other trains
    otherTrains = []
    for photo in allPhotos:
        if photo[2] not in ['Alstom Comeng', 'EDI Comeng', "X'Trapolis 100", "X'Trapolis 2.0", 'Siemens Nexas', 'HCMT', 'Sprinter', 'Vlocity', 'N Class']:
            otherTrains.append([photo[1], photo[2]])
            
    # statistics
    stats = siteStats()

    return render_template('index.html', comeng_trains=comeng, xtrap100_trains=xtrap100, siemens_trains=siemens, hcmt_trains=hcmt, xtrap2_trains=xtrap2, vlocity_trains=vlocity, sprinter_trains=sprinter, ncl_trains = ncl, otherTrains=otherTrains, linkedNumbers=withImage, stats=stats)



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
                'url': photo[7],
                'featured': photo[6],
                'note': photo[8],
                'id': photo[0]
            })
        else:
            photosInfo.append ({
                'number': photo[1],
                'type': photo[2],
                'date': photo[3],
                'location': photo[4],
                'photographer': photo[5],
                'url': photo[7],
                'featured': photo[6],
                'note': photo[8],
                'id': photo[0]
            })
    return render_template('photopage.html', info=photosInfo)

# Redirect from the old URL format
@app.route('/trains/<path:subpath>/<train_number>')
def redirect_train(subpath, train_number):
    train_number = train_number.strip('.html')
    return redirect(url_for('train_page', number=train_number), code=301)

# view counter
@app.route('/api/view/<photoID>')
@limiter.limit("100 per hour")
def count_view(photoID):
    try:
        conn = sqlite3.connect('databases/trains.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS views (
                id TEXT PRIMARY KEY,
                views INTEGER
            )
        ''')
        cursor.execute('SELECT views FROM views WHERE id = ?', (photoID,))
        result = cursor.fetchone()
    
        if result:
            new_views = result[0] + 1
            cursor.execute('UPDATE views SET views = ? WHERE id = ?', (new_views, photoID))
        else:
            cursor.execute('INSERT INTO views (id, views) VALUES (?, 1)', (photoID,))
        
        conn.commit()
        cursor.execute('SELECT views FROM views WHERE id = ?', (photoID,))
        current_views = cursor.fetchone()[0]
        return {'photoID': photoID, 'views': current_views}, 200
    
    except Exception as e:
        return {'error': str(e)}, 500
    
    finally:
        conn.close()

# image URLS for discord bot
@app.route('/api/photos/<path:filename>')
def photo_url(filename):

    urlsList = getPhotoUrls(filename)
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
            addPhoto(number, trainType, date, location, photographer, featured, image_url, note)
            
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
            'note': note
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
        


if __name__ == '__main__':
    app.run(debug=True, port=6966)