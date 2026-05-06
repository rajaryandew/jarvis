from gtts import gTTS
from pygame import mixer
import time
import os

mixer.init()
def speak(text):
    tts = gTTS(text)
    tts.save("speak.mp3")

    mixer.music.load('speak.mp3')
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(0.1)
    mixer.music.unload()
    os.remove("speak.mp3")

