from gtts import gTTS
from pygame import mixer
import time
import os
from io import BytesIO
import threading

mixer.init(frequency=88200 * 2)


def speak(text):
    fp = BytesIO()
    try:
        os.remove("speak.mp3")
    except FileNotFoundError:
        pass

    tts = gTTS(text)
    tts.write_to_fp(fp)
    fp.seek(0)

    mixer.music.load(fp, "mp3")
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(0.1)
    mixer.music.unload()

def speak_async(text):
    threading.Thread(target=speak, args=(text,)).start()


