import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from dotenv import load_dotenv
load_dotenv()

import subprocess
import speech_recognition as sr
import time
import webbrowser
from airconditioner import airconditioneraction
from ai import *
from speak import *

r = sr.Recognizer()
source = sr.Microphone()


def openspotify():
    subprocess.run("com.spotify.Client")
    speak_async("Opening spotify")


def openvim():
    subprocess.run("nvim")
    speak_async("Opening vim")


def opencode():
    subprocess.run("code")
    speak_async("Opening VS Code")


def createdir(response):
    try:
        folder_name = response.split(" ")[1]
        print(folder_name)
        os.makedirs(f"/home/raj/Documents/{folder_name}")
        speak("Created the folder successfully")
    except Exception as e:
        print(e)
        speak("It looks like the folder already exists!")


def openwebsite(response):
    url = response.split(" ")[1]
    website = response.partition(url)[2]
    speak(f"Opening {website}")
    webbrowser.open(url)


def generateSpeech(data: str):
    response: str = ask_ai(data)
    try:
        if response.startswith("WEB_ACTION"):
            openwebsite(response)
        elif response.startswith("MKDIR"):
            createdir(response)
        elif response.startswith("AC_ACTION"):
            airconditioneraction(response)
        else:
            speak(response)
    except:
        speak("Sorry, unable to do the task, try again later!")


def callback(r, audio):
    try:
        data: str = r.recognize_google(audio).lower()
        print("processing...")

        if "exit" in data:
            speak("Exitting")
            os._exit(0)
        elif "open vim" in data:
            openvim()
        elif "open code" in data:
            opencode()
        elif "open spotify" in data:
            openspotify()
        else:
            generateSpeech(data)

    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print("something went wrong", e)


# obtain audio from the microphone
print("Adjusting, waitt.....")
with source:
    r.adjust_for_ambient_noise(source, 2)
print("Say something!")
stop_listening = r.listen_in_background(source, callback)


while True:
    time.sleep(0.1)
