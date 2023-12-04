# Containerized App Exercise
[![Machine Learning Client CI](https://github.com/software-students-fall2023/4-containerized-app-exercise-team-random-seed-2/actions/workflows/ml_client_ci.yml/badge.svg)](https://github.com/software-students-fall2023/4-containerized-app-exercise-team-random-seed-2/actions/workflows/ml_client_ci.yml)

[![Web App CI/CD](https://github.com/software-students-fall2023/4-containerized-app-exercise-team-random-seed-2/actions/workflows/web_app_ci_cd.yml/badge.svg)](https://github.com/software-students-fall2023/4-containerized-app-exercise-team-random-seed-2/actions/workflows/web_app_ci_cd.yml)

<br>
This containerized application seamlessly integrates a MongoDB database, a Python Flask web app, and a machine learning client to offer efficient audio transcription services. Users upload .wav audio files to the web app, which are then transcribed into text using IBM Watson Speech to Text through the machine learning client. The transcribed data and file information is stored in MongoDB and displayed back to the user, demonstrating a robust and interactive audio-to-text conversion process.

## Group Members 
[Lara Kim](https://github.com/larahynkim) <br>
[Andrew Huang](https://github.com/andrewhuanggg) <br>
[Ahmed Omar](https://github.com/ahmed-o-324) <br>
[Henry Wang](https://github.com/fishlesswater) <br>

## Set Up Instructions 
1. The .env file for our machine-learning-client will be posted in our discord channel, randomseed2. Please download this file, then input into the project directory in the machine-learning-client sub-directory. Make sure to rename the file to .env if necessary. 

2. With Docker running, run 
```
docker-compose build
```
2. Then, run 
```
docker-compose up
```
3. Go to your browser, type "localhost:5001", and to try out the web-app and machine learning client functionalities, download a [sample audio](machine-learning-client/audio_files/audio1.wav). 

4. Click on the Upload Audio and Transcribe button to navigate to the Upload and Transcribe page. 

5. Click Choose File, then select the file, audio1.wav. 

6. Click Upload and Transcribe. 

7. To go back to the Transcript Log home page, click on the Transcript Log link. 

Please note that the machine learning client only accepts audios of .wav files. One way is to use [audacity](https://www.audacityteam.org/) to record a video message in wav format.

## Testing
1. Remember to first:
```
pip install -r requirements.txt
```
then,
```
pip install pytest
```
2.  Finally to run tests, type:
```
python -m pytest tests    
```
3. To check for coverage, 
```
python -m pip install coverage  
```
```
python -m coverage run -m pytest tests
```
```
python -m coverage report
```

## Project 4 Taskboard 
[Taskboard](https://github.com/orgs/software-students-fall2023/projects/92)

