import requests
import json

# URL of the Flask app
url = 'http://127.0.0.1:6966/upload'

# JSON data to send
data = {'number': '1M',
        'type': 'N CLass',
        'date': '2023-10-01',
        'location': 'Station A',
        'photographer': 'John Doe',
        'featured': 'Y',
        'note': 'A beautiful freight train.'}

# Files to send (replace 'sample.jpg' with a valid image path)
files = {'image': open('test.webp', 'rb')}

# Headers with the API token
headers = {'Authorization': '9L%UjyzDlk4VQJOetQ5b&DOPT*wJ&6'}

# Send POST request
response = requests.post(url, files=files, data={'data': json.dumps(data)}, headers=headers)

# Print response
print(response.json())