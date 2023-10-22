import os
from os.path import join, dirname
from dotenv import load_dotenv

from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
from datetime import datetime

""" conn = MongoClient("mongodb+srv://nirmalapusparatna20031107:npr20031107@cluster0.cqhgovi.mongodb.net/")
db = conn.dbprojects """

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def base():
    return render_template('index.html')

@app.route('/diary', methods=['POST'])
def database_post():
    image_title = request.form.get('given_img_title')
    image_desc = request.form.get('given_img_desc')
    
    # Extracting the image file
    image_file = request.files['given_img_file']
    # Extracting the image file extension
    extension_file = image_file.filename.split('.')[-1]
    # Extracting today date time (complete form)
    today = datetime.now()
    # Extracting only date and time (according format)
    the_time = today.strftime('%Y-%m-%d-%H-%M%S')
    # Arrange the file name (creating a unique filename to save in static folder)
    image_filename = f'static/post-{the_time}.{extension_file}'
    # Save the extracted image file as the 'image_filename' form
    image_file.save(image_filename)
    
    # IMAGE PROFILE
    image_profile = request.files['given_img_profile']
    # Extracting image profile photo extension
    extension_profile = image_profile.filename.split('.')[-1]
    # Arrange the file name of image profile w/ datetime addition so it becomes unique
    img_profile_filename = f'static/img_profile/post-{the_time}.{extension_profile}'
    # Save the image file in local static/img_profile folder
    image_profile.save(img_profile_filename)
    
    diary_doc = {
        'img': image_filename, # assuming just to get the data later on (not the actual image file to save in mongoDB)
        'profile': img_profile_filename,
        'title': image_title,
        'description': image_desc
    }
    
    db.diaries.insert_one(diary_doc)
    
    return jsonify({
        'msg': 'POST successfully!'
    })

@app.route('/diary', methods=['GET'])
def fetch_data():
    diary_list = list(db.diaries.find({}, {'_id': False}))
    return jsonify({
        'diaries': diary_list
    })
    
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)