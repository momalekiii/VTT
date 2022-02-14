#Developed and coded by Momalekiii
#Used libraries in this code are <--SpeechRecognition 3.8.1 & MoviePy 1.0.3-->
#follow me on all Social media as : @momalekiii


#Create a folder and put your video file and VTT.py in it then:

#First you need to import the libraries:
import sys

import speech_recognition as sr
import moviepy.editor as mp


AUDIO_FILE = "converted.wav"
RESULT_FILE = 'recognized.txt'

#handling the video file""
try:
    movie_file = sys.argv[1] # % python VTT.py movie_file
except IndexError: # no file was provided in the terminal
    movie_file = input("Put the name of your video with the extention: ").strip()

#Video to audio conversion : 
clip = mp.VideoFileClip(movie_file)
clip.audio.write_audiofile(AUDIO_FILE)


#Speech recognition :
recognizer = sr.Recognizer() 

with sr.AudioFile(AUDIO_FILE) as source:
    audio_data = recognizer.record(source)

text_result = recognizer.recognize_google(audio_data)


#Exporting the results : 
with open(RESULT_FILE,mode ='w') as file: 
   file.write("Recognized Speech:") 
   file.write("\n") 
   file.write(text_result) 
   print("Done!")
   print("I added stuff here to see if I can pull request on my own repo")

