from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime



app = Flask(__name__)
app.secret_key = 'secret_key'

# MongoDB connection
client = MongoClient("mongodb://mongodb:27017/")
db = client.transcription_database
collection = db.transcriptions

@app.route('/')
def index():
    transcriptions_list = list(collection.find().sort("timestamp", -1))
    return render_template('index.html', transcriptions=transcriptions_list)


@app.route('/record_audio')
def record_audio():
    return render_template('record_audio.html')

@app.route('/upload_transcribe', methods=['GET', 'POST'])
def upload_transcribe():
    if request.method == 'POST':
        file = request.files.get('audiofile')
        if file:
            response = send_file_to_ml_client(file)
            if response.status_code == 200:
                # Fetch the latest transcription from the database
                latest_transcription = collection.find_one(sort=[("timestamp", -1)])
                return render_template('transcription_result.html', transcription=latest_transcription)
            else:
                flash('Transcription failed')
        else:
            flash('No file selected')
    return render_template('upload_transcribe.html')

def send_file_to_ml_client(file):
    temp_filename = secure_filename(file.filename)
    file.save(temp_filename)
    with open(temp_filename, 'rb') as f:
        response = requests.post('http://ml-client:4000/transcribe', files={'file': f})
    os.remove(temp_filename) 
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
