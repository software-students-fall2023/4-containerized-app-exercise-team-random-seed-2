import io
import pytest
from unittest.mock import MagicMock, patch
from flask import Flask
from app import transcribe_audio, save_transcription_to_mongodb
from app import app as flask_app
from pymongo.errors import PyMongoError


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_transcribe_audio_success():
    # Mock successful transcription
    with patch('app.speech_to_text.recognize') as mock_recognize:
        mock_recognize.return_value.get_result.return_value = {'results': [{'alternatives': [{'transcript': 'Hello world'}]}]}
        fake_file = MagicMock()
        response = transcribe_audio(fake_file)
        assert response == {'results': [{'alternatives': [{'transcript': 'Hello world'}]}]}


def test_save_transcription_to_mongodb_failure():
    # Mock Mongo insert failure
    with patch('app.MongoClient') as mock_mongo_client:
        mock_collection = MagicMock()
        mock_collection.insert_one.side_effect = PyMongoError('MongoDB insertion failed')
        mock_mongo_client.return_value.transcription_database.transcriptions = mock_collection

        transcription_result = {'results': [{'alternatives': [{'transcript': 'Hello world'}]}]}
        filename = 'test.wav'
        response = save_transcription_to_mongodb(transcription_result, filename)

        assert response is None

def test_save_transcription_to_mongodb():
    # Mock Mongo insert
    with patch('app.MongoClient') as mock_mongo_client:
        mock_collection = MagicMock()
        mock_mongo_client.return_value.transcription_database.transcriptions = mock_collection


        transcription_result = {'results': [{'alternatives': [{'transcript': 'Hello world'}]}]}
        filename = 'test.wav'
        response = save_transcription_to_mongodb(transcription_result, filename)


        assert response is not None
        assert 'filename' in response
        assert 'transcript' in response
        assert 'timestamp' in response
        assert '_id' in response


def test_transcribe_success(client, monkeypatch):
    # Mocking transcription and Mongo insertion Succecces
    monkeypatch.setenv("API_BASE_URL", "fake_base_url")
    monkeypatch.setenv("IBM_API_KEY", "fake_api_key")


    with patch('app.transcribe_audio') as mock_transcribe_audio, \
         patch('app.save_transcription_to_mongodb') as mock_save_to_mongodb:
        mock_transcribe_audio.return_value = {'results': [{'alternatives': [{'transcript': 'Hello world'}]}]}
        mock_save_to_mongodb.return_value = {'transcription': 'fake_transcription'}


        response = client.post('/transcribe', data={'file': (io.BytesIO(b'fake_audio_data'), 'test.wav')})
        assert response.status_code == 200
        assert response.get_json() == {'transcription': {'transcription': 'fake_transcription'}}


def test_transcribe_failure(client, monkeypatch):
    # Mocking transcription failure
    monkeypatch.setenv("API_BASE_URL", "fake_base_url")
    monkeypatch.setenv("IBM_API_KEY", "fake_api_key")


    with patch('app.transcribe_audio') as mock_transcribe_audio:
        mock_transcribe_audio.return_value = None


        response = client.post('/transcribe', data={'file': (io.BytesIO(b'fake_audio_data'), 'test.wav')})
        assert response.status_code == 500
        assert response.get_json() == {'error': 'Transcription failed'}


def test_transcribe_no_file_part(client):
    response = client.post('/transcribe')
    assert response.status_code
