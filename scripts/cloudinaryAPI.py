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

def getSmallerSize(url, width, best:bool=False):
    parts = url.split('/image/upload/')
    if len(parts) != 2:
        return "Invalid URL"
    bestSTR = ''
    if best:
      bestSTR = ':best'
    new_url = f"{parts[0]}/image/upload/w_{width}/q_auto{bestSTR}/f_auto/{parts[1]}"
    return new_url