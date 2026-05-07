import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

import speech_recognition as sr
import time
import webbrowser
from ai import *
from speak import *

r = sr.Recognizer()
source = sr.Microphone()

def opencode():
    os.system("code")

def generateSpeech(data:str):
    response:str =  ask_ai(data)
    try:
        if(response.startswith("WEB_ACTION")):
            url = response.split(" ")[1]
            website = response.partition(url)[2]
            speak(f"Opening {website}")
            
            webbrowser.open(url)
        else:
            speak(response)
    except:
        speak("Sorry, unable to do the task, try again later!")


def callback(r,audio):
    try:
        data:str = r.recognize_google(audio)
        print("processing...")

        if("open code" in data):
            opencode()
        else:
            generateSpeech(data)
           
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print("something went wrong",e)

# obtain audio from the microphone
print("Adjusting, waitt.....")
with source:
    r.adjust_for_ambient_noise(source,2)
print("Say something!")
stop_listening = r.listen_in_background(source,callback,phrase_time_limit=0.5)


while True:
    time.sleep(0.1)