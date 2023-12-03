# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.

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
3. To try out the web-app and machine learning client functionalities, download a [sample audio](machine-learning-client/audio_files/audio1.wav). 

4. Click on the Upload Audio and Transcribe button to navigate to the Upload and Transcribe page. 

5. Click Choose File, then select the file, audio1.wav. 

6. Click Upload and Transcribe. 

7. To go back to the Transcript Log home page, click on the Transcript Log link. 

Please note that the machine learning client only accepts audios of .wav files. 