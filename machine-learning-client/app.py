import os
import io
from datetime import datetime
from flask import Flask, request, jsonify
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pymongo import MongoClient
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
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Directly using the uploaded file for transcription
        transcription_result = transcribe_audio(file)
        if transcription_result:
            transcription_document = save_transcription_to_mongodb(transcription_result, file.filename)
            return jsonify({'transcription': transcription_document}), 200
        else:
            return jsonify({'error': 'Transcription failed'}), 500
    except Exception as e:
        app.logger.error(f"Error during transcription process: {type(e).__name__}: {str(e)}")
        return jsonify({'error': f'Error processing audio: {type(e).__name__}: {str(e)}'}), 500

def transcribe_audio(file):
    try:
        response = speech_to_text.recognize(
            audio=file.stream, 
            content_type='audio/wav'
        ).get_result()
        return response
    except Exception as e:
        app.logger.error(f"Error during IBM Watson transcription: {type(e).__name__}: {str(e)}")
        return None


def save_transcription_to_mongodb(transcription, filename):
    client = MongoClient("mongodb://mongodb:27017/")
    db = client.transcription_database
    collection = db.transcriptions
    try:
        transcription_text = "No transcript available."
        if transcription.get('results', []) and transcription['results'][0].get('alternatives', []):
            transcription_text = transcription['results'][0]['alternatives'][0]['transcript']
        
        # Updated the structure to simplify the document
        transcription_document = {
            "filename": filename,
            "transcript": transcription_text,
            "timestamp": datetime.now()
        }
        collection.insert_one(transcription_document)
        transcription_document['_id'] = str(result.inserted_id)
        return transcription_document
    except Exception as e:
        app.logger.error(f"Error saving transcription to MongoDB: {type(e).__name__}: {str(e)}")
        return None


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4000)
