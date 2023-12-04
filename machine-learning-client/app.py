"""Module for handling audio transcription with IBM Watson Speech to Text."""
# pylint: disable=import-error
import os
from datetime import datetime

from flask import Flask, request, jsonify
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core.api_exception import ApiException
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

IBM_API_URL = os.getenv("API_BASE_URL")
IBM_API_KEY = os.getenv("IBM_API_KEY")
authenticator = IAMAuthenticator(IBM_API_KEY)
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url(IBM_API_URL)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """Handle audio file transcription request."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        transcription_result = transcribe_audio(file)
        if transcription_result:
            transcription_document = save_transcription_to_mongodb(
                transcription_result, file.filename
            )
            return jsonify({'transcription': transcription_document}), 200
        return jsonify({'error': 'Transcription failed'}), 500
    except ApiException as e:
        app.logger.error("IBM Watson API error: %s: %s", e.code, e.message)
        return jsonify({'error': 'Error with IBM Watson service'}), 500
    except PyMongoError as e:
        app.logger.error("MongoDB error: %s", str(e))
        return jsonify({'error': 'Error saving data to database'}), 500

def transcribe_audio(file):
    """Transcribe the audio file using IBM Watson."""
    try:
        response = speech_to_text.recognize(
            audio=file.stream,
            content_type='audio/wav'
        ).get_result()
        return response
    except ApiException as e:
        app.logger.error("IBM Watson API error: %s: %s",
                         e.code, e.message)
        return None

def save_transcription_to_mongodb(transcription, filename):
    """Save transcription result to MongoDB."""
    client = MongoClient("mongodb://mongodb:27017/")
    db = client.transcription_database
    collection = db.transcriptions
    try:
        transcription_text = "No transcript available."
        if transcription.get('results', []) and transcription['results'][0].get('alternatives', []):
            transcription_text = transcription['results'][0]['alternatives'][0]['transcript']
        transcription_document = {
            "filename": filename,
            "transcript": transcription_text,
            "timestamp": datetime.now()
        }
        insert_result = collection.insert_one(transcription_document)
        transcription_document['_id'] = str(insert_result.inserted_id)
        return transcription_document
    except PyMongoError as e:
        app.logger.error("MongoDB error: %s", str(e))
        return None

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4000)
