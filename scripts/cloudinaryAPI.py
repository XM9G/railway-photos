from dotenv import load_dotenv
load_dotenv()

import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api
import json


config = cloudinary.config(secure=True)

def uploadImage(filepath):

  cloudinary.uploader.upload("", public_id="quickstart_butterfly", unique_filename = False, overwrite=True)

  # Build the URL for the image and save it in the variable 'srcURL'
  srcURL = CloudinaryImage("quickstart_butterfly").build_url()

  # Log the image URL to the console. 
  # Copy this URL in a browser tab to generate the image on the fly.
  print("****2. Upload an image****\nDelivery URL: ", srcURL, "\n")