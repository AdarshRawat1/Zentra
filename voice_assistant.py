import pyttsx3
import speech_recognition as sr
import pyaudio
import wave
import threading
import io

class VoiceAssistant:
    """Handles Text-to-Speech only."""
    def __init__(self):
        try:
            self.tts_engine = pyttsx3.init()
            print("TTS engine initialized.")
        except Exception as e:
            print(f"FATAL: Could not initialize TTS engine: {e}")
            self.tts_engine = None

    def speak(self, text):
        print(f"ZENTRA 🗣️: {text}")
        if self.tts_engine:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()

class AudioRecorder:
    """A class to handle manual start/stop audio recording."""
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.is_recording = False
        self.frames = []
        self.audio_thread = None
        
        self.p_audio = pyaudio.PyAudio()
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.chunk = 1024

    def start_recording(self):
        if self.is_recording:
            return
        self.is_recording = True
        self.frames = []
        
        stream = self.p_audio.open(format=self.format, channels=self.channels,
                                   rate=self.rate, input=True,
                                   frames_per_buffer=self.chunk)
        
        def record_loop():
            while self.is_recording:
                data = stream.read(self.chunk)
                self.frames.append(data)
            stream.stop_stream()
            stream.close()

        self.audio_thread = threading.Thread(target=record_loop)
        self.audio_thread.start()
        print("Audio recording started.")

    def stop_and_transcribe(self):
        if not self.is_recording:
            return None
        self.is_recording = False
        if self.audio_thread:
            self.audio_thread.join()
        print("Audio recording stopped. Transcribing...")
        
        if not self.frames:
            print("No frames recorded.")
            return None

        audio_data_bytes = b''.join(self.frames)
        
        try:
            audio_data_obj = sr.AudioData(audio_data_bytes, self.rate, self.p_audio.get_sample_size(self.format))
            text = self.recognizer.recognize_google(audio_data_obj)
            print(f"YOU 🎙️: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None