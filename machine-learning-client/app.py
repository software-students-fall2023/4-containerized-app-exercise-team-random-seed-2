"""Transcribes audio files using the IBM Watson library and saving transcriptions to MongoDB."""

import json
import os
from datetime import datetime
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

IBM_API_URL = os.getenv('API_BASE_URL')
IBM_API_KEY = os.getenv('IBM_API_KEY')

authenticator = IAMAuthenticator(IBM_API_KEY)
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url(IBM_API_URL)

def transcribe_audio(wave_output_filename):
    """Transcribe the audio file using IBM Watson Speech to Text."""
    try:
        with open(wave_output_filename, 'rb') as audio_file:
            response = speech_to_text.recognize(
                audio=audio_file,
                content_type='audio/wav',
                model='en-US_BroadbandModel'
            ).get_result()
            return json.dumps(response, indent=2)
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return None

def save_transcription_to_mongodb(transcription, filename):
    """Save the transcription to MongoDB."""
    try:
        client = MongoClient('mongodb://host.docker.internal:27017/')
        db = client.transcription_database
        collection = db.transcriptions
        transcription_document = {
            "text": transcription,
            "timestamp": datetime.now(),
            "metadata": {
                "duration": 5,  
                "source": "file",
                "filename": filename
            }
        }
        collection.insert_one(transcription_document)
        print(f"Transcription of {filename} saved to MongoDB.")
    finally:
        client.close()

def process_audio_files(directory):
    """Process all WAV audio files in the given directory."""
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            file_path = os.path.join(directory, filename)
            transcription_result = transcribe_audio(file_path)
            if transcription_result:
                print(f"Transcription of {filename}: \n{transcription_result}")
                save_transcription_to_mongodb(transcription_result, filename)

def main():
    """Process audio files in the directory."""
    audio_files_dir = "audio_files"
    process_audio_files(audio_files_dir)

if __name__ == "__main__":
    main()
