from flask import Flask, render_template, request, redirect, url_for
#from app import process_audio_files  # import your ML client functions
from pymongo import MongoClient
import json

app = Flask(__name__)



# MongoDB connection
#client = MongoClient("mongodb://host.docker.internal:27017/")
client = MongoClient("mongodb://localhost:27017/")
db = client.transcription_database
collection = db.transcriptions





@app.route('/')
def index():
    # Fetch transcriptions from MongoDB and convert cursor to list
    transcriptions_list = list(collection.find().sort("timestamp", -1))

    # Process each transcription  
    for transcription in transcriptions_list:
        try:
            transcription['text'] = json.loads(transcription['text']) if transcription.get('text') else None
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            transcription['text'] = None

    return render_template('index.html', transcriptions=transcriptions_list)

if __name__ == '__main__':
    app.run(debug=True)



