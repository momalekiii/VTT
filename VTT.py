#Developed and coded by Momalekiii
#Used libraries in this code are <--SpeechRecognition 3.8.1 & MoviePy 1.0.3-->
#follow me on all Social media as : @momalekiii


#Create a folder and put your video file and VTT.py in it then:

#First you need to import the libraries:

import speech_recognition as sr
import moviepy.editor as mp

#Video to audio conversion : 
#Put the name of your video and extention of it between ""
clip = mp.VideoFileClip(r"NAME OF VIDEO FILE.EXTENTION")
clip.audio.write_audiofile(r"converted.wav")


#Speech recognition :
r = sr.Recognizer()
audio = sr.AudioFile("converted.wav")
with audio as source:
    audio_file = r.record(source)

result = r.recognize_google(audio_file)

result

#Exporting the results : 
with open('recognized.txt',mode ='w') as file: 
   file.write("Recognized Speech:") 
   file.write("\n") 
   file.write(result) 
   print("Done!")

