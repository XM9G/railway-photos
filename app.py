from flask import Flask, jsonify, redirect, render_template, request, url_for
from pydantic import Secret

from scripts.databaseManager import getPhotos

app = Flask(__name__)

@app.route('/')
def test_page():
    return render_template('index.html')

# Train image page
@app.route('/trains/<number>')
def train_page(number):
    photos = getPhotos(number=number)
    
    if len(photos) == 0:
        return render_template('noresults.html', number=number)
    
    photosInfo = []
    for photo in photos:
        photosInfo.append ({
            'number': photo[1],
            'type': photo[2],
            'date': photo[3],
            'location': photo[4],
            'photographer': photo[5],
            'url': photo[7],
        })
    return render_template('photopage.html', info=photosInfo)

# Redirect from the old URL format
@app.route('/trains/<path:subpath>/<train_number>')
def redirect_train(subpath, train_number):
    train_number = train_number.strip('.html')
    return redirect(url_for('train_page', number=train_number), code=301)

# image URLS for discord bot
@app.route('/photos/<path:filename>')
def photo_url(filename):
    secret = 'test'
    if secret not in request.headers:
        json = {"error": "Unauthorized"}
        return jsonify(json), 401
    else:
        return
        


if __name__ == '__main__':
    app.run(debug=True)