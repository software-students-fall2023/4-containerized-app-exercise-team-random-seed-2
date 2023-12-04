# tests/test_web_app.py

import pytest
from unittest.mock import patch, MagicMock
from werkzeug.datastructures import FileStorage
from io import BytesIO
from datetime import datetime  # Add this import for datetime
from app import (
    app as flask_app,
    index,
    upload_transcribe,
    send_file_to_ml_client,
    save_additional_data_to_mongodb,
)


@pytest.fixture
def app():
    flask_app.config["TESTING"] = True
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


# Test the index function
def test_index(client):
    with patch("app.collection.find") as mock_find:
        # Use datetime.datetime.now() to get the current datetime
        mock_find.return_value.sort.return_value = [
            {
                "transcript": "test transcript",
                "timestamp": datetime.now(),  # Correct usage of datetime
            }
        ]
        response = client.get("/")
        assert response.status_code == 200
        assert b"test transcript" in response.data


# Test the upload_transcribe function for POST request
def test_upload_transcribe_post(client):
    with patch("app.send_file_to_ml_client") as mock_send_file, patch(
        "app.collection.find_one"
    ) as mock_find_one:
        mock_send_file.return_value = MagicMock(status_code=200)
        mock_find_one.return_value = {
            "transcript": "test transcript",
            "timestamp": datetime.now(),
        }  # Correct usage of datetime
        data = {"audiofile": (BytesIO(b"fake audio data"), "test.wav")}
        response = client.post(
            "/upload_transcribe", content_type="multipart/form-data", data=data
        )
        assert response.status_code == 200
        assert b"test transcript" in response.data


# Test the save_additional_data_to_mongodb function
def test_save_additional_data_to_mongodb():
    with patch("app.collection.insert_one") as mock_insert_one:
        # Mock insert_one to return a fake InsertOneResult
        mock_insert_one.return_value = MagicMock(inserted_id="fakeid")
        save_additional_data_to_mongodb("test.wav")
        mock_insert_one.assert_called_once()
        args, kwargs = mock_insert_one.call_args
        # Check the first (and in this case, only) positional argument
        assert args[0]["file_name"] == "test.wav"  # Corrected access to the argument
