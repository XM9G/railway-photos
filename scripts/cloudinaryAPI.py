from dotenv import load_dotenv
load_dotenv()

import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api
import json


config = cloudinary.config(secure=True)

def uploadImage(filepath, id):
  upload = cloudinary.uploader.upload(filepath, public_id=id)
  return upload['secure_url']