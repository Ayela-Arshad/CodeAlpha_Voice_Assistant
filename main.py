import os
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
os.environ['QT_SCALE_FACTOR'] = '1'
os.environ['QT_SCREEN_SCALE_FACTORS'] = '1'

import sys
import webbrowser
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from PyQt5.QtWidgets import QApplication, QMainWindow
import speech_recognition as sr
import pyttsx3
import numpy as np
import scipy.io.wavfile as wav
import noisereduce as nr
from voice_assistant_ui import Ui_MainWindow

class VoiceAssistant(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_voice_assistant()
        
        # Common system applications and websites
        self.common_apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "cmd": "cmd.exe",
            "spotify" : "spotify.exe",
            "calender" : "calender.exe",
            "camera" : "camera.exe",
            "clock" : "clock.exe"
        }
        self.common_websites = {
            "youtube": "http://www.youtube.com",
            "google": "http://www.google.com",
            "gmail": "http://mail.google.com"
        }

    def init_voice_assistant(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.start_button.clicked.connect(self.start_listening)

    def start_listening(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Adjusted for ambient noise")
            self.status_label.setText("Listening...")
            QApplication.processEvents()  # Ensure the label update is shown immediately
            print("Listening...")

            self.recognizer.pause_threshold = 2  # Set the pause threshold to 1 second
            audio = self.recognizer.listen(source, phrase_time_limit=None)
            print("Audio captured")
            self.status_label.setText("Audio captured")
            QApplication.processEvents()  # Ensure the label update is shown immediately

            # Save the captured audio to a file for debugging
            with open("captured_audio.wav", "wb") as f:
                f.write(audio.get_wav_data())

            # Reduce noise in the audio
            rate, data = wav.read("captured_audio.wav")
            reduced_noise = nr.reduce_noise(y=data, sr=rate)
            wav.write("reduced_noise.wav", rate, reduced_noise)

            # Load the noise-reduced audio
            with sr.AudioFile("reduced_noise.wav") as source:
                audio = self.recognizer.record(source)

            try:
                command = self.recognizer.recognize_google(audio)
                print("Recognized Command:", command)
                self.status_label.setText(f"Recognized Command: {command}")
                self.process_commands(command)
            except sr.UnknownValueError:
                print("UnknownValueError: Could not understand audio")
                self.status_label.setText("Could not understand audio")
                self.speak("Sorry, I did not understand that.")
            except sr.RequestError as e:
                print(f"RequestError: {e}")
                self.status_label.setText("Speech service is down")
                self.speak("Sorry, my speech service is down.")

            QApplication.processEvents()  # Ensure the label update is shown immediately

    def process_commands(self, command):
        print(f"Processing Commands: {command}")
        commands = command.lower().split(" and ")
        for cmd in commands:
            app_match = process.extractOne(cmd, self.common_apps.keys(), scorer=fuzz.partial_ratio)
            if app_match and app_match[1] > 80:
                app = self.common_apps[app_match[0]]
                self.open_application(app)
                continue
            
            website_match = process.extractOne(cmd, self.common_websites.keys(), scorer=fuzz.partial_ratio)
            if website_match and website_match[1] > 80:
                url = self.common_websites[website_match[0]]
                self.open_website(url)
                continue
            
            self.speak(f"I am sorry, I do not have a function for the command: {cmd}")

    def open_application(self, app):
        self.speak(f"Opening {app}")
        os.system(app)
    
    def open_website(self, url):
        self.speak(f"Opening {url}")
        webbrowser.open(url)
    
    def speak(self, text):
        print(f"Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoiceAssistant()
    window.show()
    sys.exit(app.exec_())
