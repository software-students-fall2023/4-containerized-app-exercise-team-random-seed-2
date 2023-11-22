import json
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('API_BASE_URL')
key = os.getenv('IBM_API_KEY')

authenticator = IAMAuthenticator(key)
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url(url)

def transcribe_audio(wave_output_filename):
    """Transcribe the audio file using IBM Watson Speech to Text."""
    with open(wave_output_filename, 'rb') as audio_file:
        try:
            response = speech_to_text.recognize(
                audio=audio_file,
                content_type='audio/wav',
                model='en-US_BroadbandModel'
            ).get_result()
            return json.dumps(response, indent=2)
        except Exception as e:
            print(f"Error: {e}")
            return None

def save_transcription_to_mongodb(transcription, filename):
    """Save the transcription to MongoDB."""
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
    print("Transcription saved to MongoDB.")

def main():
    audio_files_dir = "audio_files"  
    for filename in os.listdir(audio_files_dir):
        if filename.endswith(".wav"):  
            file_path = os.path.join(audio_files_dir, filename)
            transcription_result = transcribe_audio(file_path)
            if transcription_result:
                print("Transcription of {}: \n{}".format(filename, transcription_result))
                save_transcription_to_mongodb(transcription_result, filename)

if __name__ == "__main__":
    main()
