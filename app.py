from flask import Flask, jsonify, redirect, render_template, request, send_file, url_for
from pydantic import Secret

from scripts.databaseManager import getPhotoUrls, getPhotos, siteStats
from scripts.trainLists import getSets

app = Flask(__name__)

@app.route('/')
def test_page():
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

    for train in comeng + xtrap100 + siemens + hcmt + xtrap2 + vlocity + sprinter+ ncl:
        if isinstance(train['cars'], str):
            train['cars'] = train['cars'].split('-')
        elif isinstance(train['cars'], list) and len(train['cars']) == 1 and '-' in train['cars'][0]:
            train['cars'] = train['cars'][0].split('-')
            
    # statistics
    stats = siteStats()

    return render_template('index.html', comeng_trains=comeng, xtrap100_trains=xtrap100, siemens_trains=siemens, hcmt_trains=hcmt, xtrap2_trains=xtrap2, vlocity_trains=vlocity, sprinter_trains=sprinter, ncl_trains = ncl, linkedNumbers=withImage, stats=stats)



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
            })
    return render_template('photopage.html', info=photosInfo)

# Redirect from the old URL format
@app.route('/trains/<path:subpath>/<train_number>')
def redirect_train(subpath, train_number):
    train_number = train_number.strip('.html')
    return redirect(url_for('train_page', number=train_number), code=301)

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
        


if __name__ == '__main__':
    app.run(debug=True, port=6966)