#Developed by Momalekiii


import moviepy.editor as mp
import speech_recognition as sr

def main():
    clip = mp.VideoFileClip(r"video.mp4")  # add video name here
    clip.audio.write_audiofile(r"converted.wav")


recognizer = sr.Recognizer()
    audio = sr.AudioFile("converted.wav")
    with audio as source:
        audio_file = recognizer.record(source)

result = recognizer.recognize_google(audio_file)

 with open("recognized.txt", mode="w") as file:
        file.write("Recognized Speech:")
        file.write("\n")
        file.write(result)
        print("Done!")


if __name__ == '__main__':
    main()

